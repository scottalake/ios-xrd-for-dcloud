# -----------------------------------------------------------------------------
# ctre.py - Container Rebuild tool
#
# May 2022, Joe Jenne
#
# Copyright (c) 2022 by cisco Systems, Inc.
# All rights reserved.
# -----------------------------------------------------------------------------

"""
Container Rebuild tool

Simplest usage:
    1. User has a container image built and loaded for the current workspace.
    2. User modifies a file fixing up a failure noticed during launch.
    3. User runs 'ctre'
    4. User runs 'launch-xrd rebuild'

NOTE: Supports python 3.9+.
If in sparse workspace, this script would ideally have package/version_labels.
"""

__all__ = ("rebuild_container", "Error")


import argparse
import contextlib
import collections
import json
import subprocess
import sys
import tempfile
import typing
from pathlib import Path
from typing import Iterable, Generator, Optional, Sequence, TypedDict

_Components = dict[Path, set[Path]]
DEFAULT_TAG = "ctre"
LABEL_FILE = "package/version_labels/src/version_labels.txt"
COMPILED_SUFFIXES = {".c", ".h", ".bag", ".enumh", ".msg"}
OBJ_DIR = "obj-x86_64-thinxr"


class Error(Exception):
    """Standard error raised by something the script expects may go wrong."""


class Export(TypedDict):
    """An 'export' data mapping found in a comp-mdata.pl file."""

    name: str
    router_name: str
    relative_dir: str
    target_dir: str
    absolute_target_dir: str
    is_not_derived: int


@contextlib.contextmanager
def tmpdir(ws_root: Path) -> Generator[Path, None, None]:
    """
    Wrapper of 'TemporaryDirectory' that uses pathlib.Path instead of the
    tempfile custom type.

    NOTE: The wrapper creates the temp dir in the workspace as cross-device
    (/nobackup to /tmp) hardlinking is not possible.
    """
    with tempfile.TemporaryDirectory(dir=ws_root) as my_dir:
        yield Path(my_dir)


@contextlib.contextmanager
def cleanup_tag(tag: str) -> Generator[None, None, None]:
    """
    Tag the previous rebuild image to be cleaned up when leaving the context.

    The 'rmi' command deletes the image if X is the only tag pointing at the
    image, if another tag points at the same image then X is just untagged.

    Ignore failures to tag the image as it just means there is no previous
    rebuild to cleanup after.
    """
    try:
        subprocess.check_output(
            ["docker", "image", "tag", tag, f"{tag}:rm"],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError:
        pass
    try:
        yield
    finally:
        subprocess.check_output(
            ["docker", "image", "rmi", "--force", f"{tag}:rm"],
            stderr=subprocess.STDOUT,
        )


def _colour(string: str, colour_code: int, style: int = 0) -> str:
    if sys.stdout.isatty():
        return f"\033[{style};{colour_code}m{string}\033[0m"
    else:
        return string


def red(string: str) -> str:
    return _colour(string, 31, 1)


def yellow(string: str) -> str:
    return _colour(string, 33)


def green(string: str) -> str:
    return _colour(string, 32)


def warn(msg: str) -> None:
    print(f"{yellow('Warning:')} {msg}", file=sys.stderr)


def cmd_is_ok(cmd: list[str]) -> bool:
    """True if cmd returns zero or False if the command errors."""
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False


def parse_args() -> argparse.Namespace:
    """Process command line arguments"""
    parser = argparse.ArgumentParser(
        prog="ctre",
        description="ConTainer REbuilder - guesses what needs to be built, can simply run 'ctre'. "
        "Limitations: Jam is not run so will only copy non-derived files e.g. "
        ".sh, .py, .yaml, etc. you will have to build a new container to see compiled file changes.",
    )
    parser.add_argument(
        "-i",
        "--image",
        metavar="IMG",
        help="loaded docker image name to build from (defaults to the current EFR's image)",
    )
    parser.add_argument(
        "-t",
        "--tag",
        default=DEFAULT_TAG,
        help=f"tag for the rebuilt image, or image to clean (defaults to '{DEFAULT_TAG}')",
    )
    parser.add_argument(
        "--from-build",
        action="store_true",
        help="add build artifacts (in espresso) to the files found by git, to copy into the image",
    )
    parser.add_argument(
        "-E",
        "--exclude",
        type=Path,
        action="append",
        help="exclude files used in rebuild by directory or individual file paths",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print the generated Dockerfile before building",
    )
    parser.add_argument(
        "files",
        nargs="*",
        default=[],
        type=Path,
        help="files to be copied into the rebuilt container - relative to ws-root "
        "(defaults to the files touched/added on the EFR)",
    )
    return parser.parse_args()


def list_images() -> list[str]:
    """List loaded docker images."""
    return subprocess.check_output(
        "docker images --filter='dangling=false' | sed -nr '1!s/ +/:/p' | awk '{print $1}'",
        shell=True,
        text=True,
    ).splitlines()


def guess_images() -> list[str]:
    """
    Guess a sequence of potential loaded image names in order of preference.

    1. The name used in the developer workflow (launch-xrd-dev)
    2. The image label corresponding to the packaged XR version

    For (2), it is assumed that the image loaded that needs to be rebuilt is
    built for the current EFR. The version_labels.txt file can therefore be
    read and the '[XR_LABEL] :  [7.8.1.11I]' line parsed for the full XR
    version label.
    """
    dev_label = subprocess.check_output(
        "platforms/espresso/tools/image-name", text=True
    ).strip()
    images = [dev_label]

    if not Path(LABEL_FILE).exists():
        warn(
            f"Missing {LABEL_FILE}. Cannot guess image name using XR version."
        )
    else:
        pkg_label = subprocess.check_output(
            ["sed", "-nr", r"s/\[XR_LABEL\] *: *\[(.*)\]/\1/p", LABEL_FILE],
            text=True,
        )
        images.append(f"localhost/ios-xr:{pkg_label.strip()}")

    return images


def get_first_loaded_image(
    images: Sequence[str], guessed: bool = False
) -> str:
    """
    Return the first image name of the input sequence that has been loaded into
    docker.

    Raise an error if none exist, and print some debug for the user if the
    first loaded image name was guessed.
    """
    for image in images:
        if cmd_is_ok(["docker", "image", "inspect", image]):
            if guessed:
                print(
                    f"Image '{image}' guessed from local XR package version."
                )
            return image

    if guessed:
        maybe_guessed = "guessed "
    else:
        maybe_guessed = ""

    if len(images) > 1:
        image_or_images = "images"
    else:
        image_or_images = "image"

    known_images = ", ".join(list_images() or ("None",))

    raise Error(
        f"Unknown {maybe_guessed}{image_or_images}: {', '.join(images)}.\n"
        f"Known: {known_images}"
    )


def get_git_files(*, diff_filter: str = "AM") -> list[Path]:
    """
    List the paths that git knows are <verb>-ed since the EFR tag.

    The <verb> depends on the "diff filter" which defaults to 'AM' (files that
    are added or modified). Filter 'D' (deleted files) is also useful.
    """
    return [
        Path(file)
        for file in subprocess.check_output(
            f'git diff --name-only --diff-filter={diff_filter} "$(cat .XR_WSROOT/EFR)"',
            shell=True,
            text=True,
        ).splitlines()
    ]


def get_built_files() -> list[Path]:
    """Get all files in obj-* directories (in a "directory to check")."""
    directory_to_check = "platforms/espresso"
    return [
        Path(file)
        for file in subprocess.check_output(
            [
                "/auto/smartdev/bin/fd",
                OBJ_DIR,
                "--full-path",
                "--no-ignore",
                "--type=file",
                directory_to_check,
            ],
            text=True,
        ).splitlines()
    ]


def filter_excludes(
    files: list[Path], excludes: list[Path], *, verbose: bool = False
) -> list[Path]:
    """Filter the file list using a list of dirs/files to exclude."""
    files_to_use = [
        file
        for file in files
        for exclude in excludes
        if not file.is_relative_to(exclude)
    ]
    if verbose:
        used = set(files_to_use)
        not_used = "\n - ".join(str(f) for f in files if f not in used)
        print(f"Excluding the following files:\n - {not_used}")
    else:
        print(
            f"Excluding {len(files) - len(files_to_use)} files (see --verbose)"
        )

    return files_to_use


def get_ws() -> Path:
    """Return the path of the workspace root (the current git repo)."""
    return Path(
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
    )


def get_exports(compmdata: Path) -> list[Export]:
    """
    Use a perl one-liner to convert a comp-mdata.pl's @Exports into a python
    object via JSON.
    """
    js = subprocess.check_output(
        [
            "perl",
            "-e",
            rf"use JSON; do '{compmdata}'; print JSON->new->encode(\@Exports);",
        ]
    )
    return typing.cast(list[Export], json.loads(js))


def export_name(export: Export) -> str:
    """Get the name of a comp-mdata.pl export - name field is always present."""
    return export["name"].replace(".dll", ".so")


def get_ctr_path(export: Export) -> Path:
    """Get the full router/container path of an exported artifact."""
    if "target_dir" in export:
        router_dir = Path("/pkg") / export["target_dir"]
    else:
        abs_tgt_dir = export.get("absolute_target_dir")
        assert abs_tgt_dir, "Must specify abs tgt dir if not rel."
        router_dir = Path(abs_tgt_dir)

    return router_dir / export.get("router_name", export_name(export))


def get_ws_path(component: Path, export: Export) -> Path:
    """
    Get full path to an exported artifact in the workspace.

    If an export is derived (built with Jam), it is in an obj dir.
    """
    name = export_name(export)
    wsdir = component / export.get("relative_dir", "")

    if export.get("is_not_derived", 0):
        return wsdir / name
    else:
        return wsdir / OBJ_DIR / name


def get_comp_path_map(component: Path) -> dict[Path, Path]:
    """
    By parsing the comp-mdata, map a component's packaged files to their ctr path.
    """
    return {
        get_ws_path(component, export): get_ctr_path(export)
        for export in get_exports(component / "comp-mdata.pl")
    }


def get_component_from_path(path: Path) -> Path:
    """Find the first parent directory that has a comp-mdata.pl file."""
    end = Path("/")
    component = path.parent
    while True:
        if (component / "comp-mdata.pl").exists():
            return component
        elif component == end:
            raise Error(f"Not in component: {path}")
        else:
            component = component.parent


def check_missed_files(
    components: _Components, files_to_copy: set[Path]
) -> None:
    """
    Warn to stderr if any of the input files (by component) are not be copied
    into the rebuilt container.
    """
    for component, input_files in components.items():
        if missing := input_files - files_to_copy:
            not_found = "\n - ".join(str(m) for m in missing)
            warn(
                "These files are input but NOT being copied (not packaged in "
                f"{component/'comp-mdata.pl'}):\n - {not_found}"
            )


def check_suffixes(files: Iterable[Path]) -> Optional[str]:
    """
    Return a warning string if any touched files contain suffixes of compiled
    files.
    """
    compiled_files = {f for f in files if f.suffix in COMPILED_SUFFIXES}

    if compiled_files:
        return (
            f"{len(compiled_files)} compiled files are not rebuilt or copied"
            " into the image (see --verbose)."
        )
    else:
        return None


def check_same_dest(
    path_mappings: dict[Path, Path], detailed_warning: bool = False
) -> None:
    """
    Examine the path mappings for multiple workspace files packaged
    to the same router location, overwriting another due to no platform
    separation.
    """
    pkg_from = collections.defaultdict(list)

    for ws_path, ctr_path in path_mappings.items():
        pkg_from[ctr_path].append(ws_path)

    multi_pkg_from = {
        pkg: places for pkg, places in pkg_from.items() if len(places) > 1
    }

    if multi_pkg_from:
        if detailed_warning:
            msg = ["Multiple files packaged to same location:"]
            for pkg, places in multi_pkg_from.items():
                msg.append(f" - {pkg}")
                msg.extend(
                    (f"     {n+1}. {place}" for n, place in enumerate(places))
                )
            warn("\n".join(msg))
        else:
            warn(
                "Multiple files packaged to the same location (see --verbose)"
            )


def gen_dockerfile(
    ws_root: Path,
    image: str,
    files: Iterable[Path],
    *,
    detailed_warning: bool = False,
) -> str:
    """
    Generate a Dockerfile basing off our image, copying files in.

    Comp-mdata files are parsed to work out the relevant files and where they
    belong inside the image.

    The logic is effectively:
        For all files exported in the input comp-mdata.pl, if any of the
        constructed internal workspace paths match a path we care about,
        include that path in our returned mapping.
    """
    # Mapping from component path to input files that _may_ be packaged in it.
    components: _Components = collections.defaultdict(set)
    for file in files:
        components[get_component_from_path(file)].add(file)

    # Filter all component path mappings using our input files.
    path_mappings = {
        ws_path: ctr_path
        for comp, files in components.items()
        for ws_path, ctr_path in get_comp_path_map(comp).items()
        if ws_path in files
    }

    if detailed_warning:
        check_missed_files(components, set(path_mappings))
    check_same_dest(path_mappings, detailed_warning)

    lines = ["# Generated Dockerfile (ctre)", f"FROM {image}"]
    lines.extend(
        (
            f"COPY {ws_path.relative_to(ws_root)} {ctr_path}"
            for ws_path, ctr_path in path_mappings.items()
        )
    )
    return "\n".join(lines)


def build(builddir: Path, tag: str = DEFAULT_TAG) -> None:
    """Run a docker build in a given dir, tagging the loaded image."""
    subprocess.check_output(
        ["docker", "build", "./", "--tag", tag], cwd=builddir
    )


def rebuild_container(
    ws_root: Path,
    image: str,
    files: Iterable[Path],
    tag: str = DEFAULT_TAG,
    *,
    verbose: bool = False,
    is_manual: bool = False,
) -> None:
    """
    Rebuild the container in a temporary build directory in three stages:
      1. Generate a Dockerfile based on the input files
      2. Link the input files into the directory in their workspace paths
      3. Run the docker build command

    NOTE: This function assumes that the input "files" are absolute and in the
    same workspace as the cwd.

    :param verbose:
        True if more details are required in console output.

    :param is_manual:
        Set True if the input files are manually specified on the command line.
        More care is taken when ignoring the input files when manual.
    """
    dockerfile = gen_dockerfile(
        ws_root, image, files, detailed_warning=(verbose or is_manual)
    )
    if verbose:
        print(dockerfile)

    with tmpdir(ws_root) as builddir:
        (builddir / "Dockerfile").write_text(dockerfile)
        for file in files:
            # Link $ws/foo/bar/baz.py into $ws/tmpXX/foo/bar/baz.py
            link_loc = builddir / file.relative_to(ws_root)
            link_loc.parent.mkdir(parents=True, exist_ok=True)
            file.link_to(link_loc)
        build(builddir, tag)


def main() -> None:
    """
    Main argument parsing, validation and calling of the rebuild_container API.

    Two modes of file selection: manual and git based. The choice affects how
    the user is warned too.
    """
    args = parse_args()

    if args.image:
        images = [args.image]
        guessed_image = False
    else:
        images = guess_images()
        guessed_image = True

    image = get_first_loaded_image(images, guessed_image)

    if args.files:
        files: list[Path] = args.files
        for file in files:
            if not file.exists():
                raise Error(f"No such file or directory: '{file}'")
    else:
        files = get_git_files()
        print(f"Using the {len(files)} files touched on this EFR.")
        if not args.verbose and (warning := check_suffixes(files)):
            warn(warning)
        if (
            removed_files := get_git_files(diff_filter="D")
        ) and not args.verbose:
            warn(
                f"{len(removed_files)} removed files may remain in the image if "
                "packaged (see --verbose)."
            )
        elif removed_files and args.verbose:
            warn(
                "These files are removed but _may_ still be in the image after rebuild:\n"
                + "\n".join((f" - {f}" for f in removed_files))
            )

    if args.from_build:
        files.extend(get_built_files())

    if args.exclude:
        files = filter_excludes(files, args.exclude, verbose=args.verbose)

    ws_root = get_ws()
    abs_files = [f if f.is_absolute() else ws_root / f for f in files]

    with cleanup_tag(args.tag):
        rebuild_container(
            ws_root,
            image,
            abs_files,
            args.tag,
            verbose=args.verbose,
            is_manual=bool(args.files),
        )
    print(f"{green('Success!')} Now: launch-xrd {args.tag}")


if __name__ == "__main__":
    try:
        main()
    except Error as e:
        print(f"{red('ERROR:')} {e}", file=sys.stderr)
        sys.exit(1)
