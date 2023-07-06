import os
import signal
import subprocess
import argparse
from git import Repo
from git import GitCommandError
from dotenv import load_dotenv
from modules.GitHub_Helpers import *

# Load environment variables from .env file
load_dotenv()

# Get the GitHub token from environment variables
github_token = os.getenv("GITHUB_TOKEN")
github_username = os.getenv("GITHUB_USERNAME")

# Define Helper Functions

# Define a flag for SIGKILL received
sigkill_received = False


# Graceful Stop - Handle SIGKILL signal
def handle_sigint(signal, frame):
    print("SIGINT received. Stopping script...")
    global sigkill_received
    sigkill_received = True
    exit(0)


# Check if git-lfs is installed
def is_git_lfs_installed():
    """
    Check if git-lfs is installed.
    :return: True if git-lfs is installed, False otherwise
    """
    try:
        subprocess.check_output(["git", "lfs", "--version"])
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


# Begin main script

# Register the SIGINT handler
signal.signal(signal.SIGINT, handle_sigint)

# Check if git-lfs is installed
if not is_git_lfs_installed():
    print("Git LFS is not installed. Please install Git LFS and try this command again.")
    exit(1)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="GitHub Team Repository Backup Script")
parser.add_argument("--repos-directory", type=str, required=True, help="Directory to store the local clones")
parser.add_argument("--team-name", type=str, required=True, help="GitHub team name")
parser.add_argument("--org-name", type=str, required=True, help="GitHub organization or user name")
args = parser.parse_args()

# Set command-line argument values
repos_directory = args.repos_directory
team_name = args.team_name
org_name = args.org_name

# Get SSH URLs for team repositories
url_list = get_https_urls_for_team_repositories(github_username, github_token, org_name, team_name)

# A simple counter to stop after a certain number of repositories. Set to 0 to disable.
# Useful for testing.
stop_after_count = 2
repo_count = 0

# Welcome message
print(f'Backing up from GitHub organization: "{org_name}", team" "{team_name}"')
print(f'Backing up to: "{repos_directory}"\n')

# Iterate over the SSH URLs
for repo_url in url_list:
    repo_count += 1
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    local_path = os.path.join(repos_directory, repo_name)

    if os.path.exists(local_path):
        print(f"Updating {repo_name}...")
        try:
            # Fetch the latest changes
            repo = Repo(local_path)
            repo.remotes.origin.fetch()
            # Fetch Git LFS objects
            os.chdir(local_path)
            os.system("git lfs fetch --all")
        except Exception as e:
            print(f"General error: {str(e)}")
        except GitCommandError as e:
            print(f"Git command error: {str(e)}")
    else:
        print(f"Cloning {repo_name}...")
        try:
            # Clone the repository (in MIRROR mode)
            Repo.clone_from(repo_url, local_path, mirror=True)
            # Fetch Git LFS objects
            os.chdir(local_path)
            os.system("git lfs fetch --all")
        except Exception as e:
            print(f"General error: {str(e)}")
        except GitCommandError as e:
            print(f"Git command error: {str(e)}")

    print(f"Done with {repo_name}.\n")

    # Check if SIGKILL was received and stop if it was
    if sigkill_received:
        break

    # If stop_after_count is set and we've reached that number of repositories, stop
    if 0 < stop_after_count <= repo_count:
        break
