import subprocess
import os

def build_project(id):
    # Construct the directory path
    directory_path = os.path.join(os.path.dirname(__file__), f"output\{id}")

    # Debugging: Print the constructed directory path
    print("Constructed directory path:", directory_path)

    # Execute the npm commands using subprocess with the specified working directory
    try:
        child = subprocess.Popen('install npm && npm build run', shell=True, cwd=directory_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Handle stdout
        for line in child.stdout:
            print('stdout:', line.decode().strip())

        # Handle stderr
        for line in child.stderr:
            print('stderr:', line.decode().strip())

        # Wait for the process to finish and get the return code
        code = child.wait()

        print("Process completed with code:", code)
    except Exception as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    build_project("eK1Nm")
