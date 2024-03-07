import subprocess
import os
import shutil

def buildReact(id):
    # Define the source directory containing the project files
    source_dir = os.path.join(os.path.dirname(__file__), f'output/{id}')

    # Execute npm install and npm run build in the source directory
    command = f'cd {source_dir} && npm install && npm run build'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Read stdout and stderr asynchronously
    while True:
        stdout = process.stdout.readline().decode('utf-8')
        stderr = process.stderr.readline().decode('utf-8')

        if process.poll() is not None and not stdout and not stderr:
            break

        if stdout:
            print('stdout:', stdout.strip())
        if stderr:
            print('stderr:', stderr.strip())

    # Define the destination directory where the build files should be moved
    destination_dir = os.path.join(os.getcwd(), 'DeployService', 'Build', id)

    # Ensure that the destination directory does not exist
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    source_dir = os.path.join(source_dir,'dist')
    # Move files and directories from source to destination
    shutil.move(source_dir, destination_dir)

