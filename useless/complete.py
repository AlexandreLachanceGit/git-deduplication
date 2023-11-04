import os
import subprocess

# Replace this with the path to your directory containing Git repositories
directory_path = "repos/"

# Get a list of all subdirectories in the specified directory
subdirectories = os.scandir(directory_path) 


for repo_dir in subdirectories:
    print(repo_dir)
    # Change the current working directory to the Git repository
    os.chdir(repo_dir)

    # Run "git pull" using the subprocess module
    result = subprocess.run(["git", "pull", "--unshallow"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Print the output of the "git pull" command
    print(f"Repository: {repo_dir}")
    print(result.stdout.decode('utf-8'))
    print(result.stderr.decode('utf-8'))
    print("=" * 40)
    os.chdir("../..")

