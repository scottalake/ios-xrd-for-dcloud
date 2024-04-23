from flask import Flask, render_template, jsonify, send_from_directory, redirect
import subprocess
import shlex
import os

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle silent SSH command execution
@app.route('/run_ssh_command', methods=['GET'])
def run_ssh_command():
    # Define your SSH command and credentials here
    ssh_password = 'cisco123'
    ssh_user = 'dcloud'
    ssh_host = '198.18.133.20'
    ssh_command = 'ls -la'  # The command to be executed on the remote host

    # Construct the sshpass command
    command = f"sshpass -p {ssh_password} ssh {ssh_user}@{ssh_host} '{ssh_command}'"
    
    # Use shlex to safely parse the string into a command list
    command_list = shlex.split(command)
    
    # Execute the command and capture the output
    try:
        output = subprocess.check_output(command_list, stderr=subprocess.STDOUT)
        # Since no feedback is necessary, just return success status
        return jsonify({'status': 'success'})
    except subprocess.CalledProcessError as e:
        # Log error and return failure status
        print(f"Error executing SSH command: {e.output}")
        return jsonify({'status': 'error'}), 500
    

# Route for serving static files (e.g., JavaScript, CSS)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Route to redirect to the web-based SSH client
@app.route('/ssh-client')
def ssh_client():
    # Replace this with the actual URL of your web-based SSH client
    web_ssh_client_url = os.getenv('COCKPIT_URL', 'https://localhost:9090')
    return redirect(web_ssh_client_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
