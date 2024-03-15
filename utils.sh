# shellcheck shell=bash
#------------------------------------------------------------------------------
# utils.sh - Utility functions for developer scripts
#
# May 2021, Lewis Gaul
#
# Copyright (c) 2021-2022 by cisco Systems, Inc.
# All rights reserved.
#------------------------------------------------------------------------------

# Supported xrd platforms
PLATFORMS=("xrd-control-plane" "xrd-vrouter")

get_supported_platforms() {
    echo "${PLATFORMS[*]}"
}

is_supported_platform() {
    PLATFORM="$1"
    for plat in "${PLATFORMS[@]}"; do
        if [[ "$plat" == "$PLATFORM" ]]; then
            return 0
        fi
    done
    return 1
}

find_ws_root() {
    local WORKSPACE=$PWD
    while [[ ! -d "$WORKSPACE/.ACMEROOT" ]]; do
        WORKSPACE=$(dirname "$WORKSPACE")
        if [[ "$WORKSPACE" == '/' ]]; then
            return 1
        fi
    done
    echo "$WORKSPACE"
}

# Quote a bash command - the output can be directly run.
_quote_cmd() {
    # Python's shlex module is used as it gives cleaner output than bash's
    # 'printf "%q " "$@"' (quotes rather than backslash escapes).
    python3 -c \
        'import shlex, sys; print(" ".join(shlex.quote(x) for x in sys.argv[1:]))' \
        "$@"
}

# Either run the given command or output the command on stderr if DRY_RUN=1.
_runcmd() {
    if [[ $DRY_RUN == 1 ]]; then
        _quote_cmd "$@"
    else
        "$@"
    fi
}

# Get the platform from the labels on a container image
# Args:
#   $1: image name
_get_platform() {
    local platform
    local image_name="$1"
    local container_mgr="${CONTAINER_MGR:-docker}"

    platform="$($container_mgr inspect "$image_name" \
        --format='{{index .Config.Labels "com.cisco.ios-xr.platform"}}' 2>/dev/null)"
    # Assert that the container image has the word "xrd" in it.
    if [[ $platform != *xrd* ]]; then
        echo "Error: Could not determine platform from image '$image_name' labels." >&2
        echo "Use '--platform' argument instead." >&2
        exit 1
    fi
    echo -n "$platform"
}

# Get the path to the container source in the img-* directory
# Args:
#   $1: XR packaging platform name
_img_dir_source() {
    local platform="$1"
    echo "img-$platform/$platform-container-x64.dockerv1.tgz"
}

# Copy any files that are expected to be local to the docker daemon.
# Also involves checking the docker host is reachable and giving a friendly
# error message if not!
copy_files_to_docker_host() {
    if [[ $DOCKER_HOST =~ ^ssh:// ]]; then
        local host_addr=${DOCKER_HOST#ssh://}
        local host port
        if [[ $host_addr == *:* ]]; then
            host=${host_addr%:*}
            port=${host_addr#$host:}
        else
            host=$host_addr
            port=""
        fi
        local ssh_opts=(
            "-oStrictHostKeyChecking=no" "-oUserKnownHostsFile=/dev/null"
            "-oLogLevel=ERROR" "-oPasswordAuthentication=no")
        local ssh_cmd=(ssh "$host" "${ssh_opts[@]}")
        local scp_cmd=(scp "${ssh_opts[@]}")
        if [[ $port ]]; then
            ssh_cmd+=("-p" "$port")
            scp_cmd+=("-P" "$port")
        fi
        if ! "${ssh_cmd[@]}" true > /dev/null; then
            echo "Unable to connect to DOCKER_HOST '$host_addr' over SSH" >&2
            return 1
        fi

        for file in "$@"; do
            if [[ ! -f $file ]]; then
                echo "File not found: $file" >&2
                return 1
            fi
            # Get the full path of the file so it's copied to where we expect
            # it in launch-xrd
            file=$(realpath "$file")
            # Use 'printf %q' to escape spaces in the remote command.
            local remote_file=$(printf %q "$file")
            local remote_dir=$(printf %q "$(dirname "$file")")
            if ! "${ssh_cmd[@]}" "ls $remote_dir" &> /dev/null; then
                "${ssh_cmd[@]}" "mkdir -p $remote_dir" || return 1
            fi
            # Copy file to remote if it doesn't exist or is out of date.
            if ! "${ssh_cmd[@]}" "ls $remote_file" &> /dev/null || \
               [[ $(stat -c %Y "$file") -gt $("${ssh_cmd[@]}" "stat -c %Y $remote_file") ]]
            then
                echo "Copying $file to docker host $host_addr"
                "${scp_cmd[@]}" "$file" "$host:$file" > /dev/null || return 1
            else
                echo "$file already up to date on docker host $host_addr"
            fi
        done
    fi
}

# Find a platform using an optional image or build outputs
# Args:
#   $1: Loaded container image name (Optional)
# First, if the image is passed get the platform from inspecting the
# container's label. If the image is not passed, check, across supported
# platforms, for the container tarball output by the build in img-*
# directories. Error if:
#   a) The container's platform label cannot be parsed
#   b) Multiple tarballs exist in the workspace, user must be explicit
#   c) No tarballs exist in the workspace, no image can be found
_find_platform () {
    local image_name="$1"
    local plat_to_check
    local platform
    local img_source

    if [[ $image_name ]]; then
        # work out platform from inspecting the image
        if ! platform="$(_get_platform "$image_name")"; then
            return 1
        fi
    else
        for plat_to_check in $(get_supported_platforms); do
            img_source="$WS_ROOT"/"$(_img_dir_source "$plat_to_check")"
            if [[ -e $img_source && ! $platform ]]; then
                platform="$plat_to_check"
            elif [[ -e $img_source && $platform ]]; then
                # User has mutliple img-*/*-container.dockerv1.tgz sources in
                # the workspace. Therefore cannot calculate which one to use.
                echo "Cannot guess desired platform. Multiple XRd platforms appear to have been built:" >&2
                echo "    $(_img_dir_source "$platform") and $(_img_dir_source "$plat_to_check")." >&2
                echo "" >&2
                echo "Pass the --platform arg in this instance to pick up the correct file." >&2
                return 1
            fi
        done
        # No image specified
        if [[ ! $platform ]]; then
            # No img-xrd*/*-container.dockerv1.tgz containers to load.
            echo "Cannot guess desired platform. No XRd platforms appear to have been built." >&2
            echo "An image can be explicitly passed with --image." >&2
            return 1
        fi
    fi

    echo "$platform"
}
