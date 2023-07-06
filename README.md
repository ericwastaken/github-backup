# README

## Summary

Given a git username or organization name, and team, backs up all the repositories for that team to a local directory. The backup scripts uses a GitHub MIRROR to create a clean backup of the repository with all history and branches. The backup script also uses git-lfs to back up any large files that are stored in the repository.

It Can be run repeatedly to update the local backup with the latest changes.

This script loosely implements the instructions found in [GitHub Docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository#mirroring-a-repository).

Note; despite having a similar name, this repo is not related to any of the following, all of which appear to be much more complete GitHub backup tools also in Python.

- https://github.com/josegonzalez/python-github-backup
- https://github.com/clockfort/GitHub-Backup

## GitHub Authentication

The backup script needs to authenticate to GitHub. It does this by using a GitHub Personal Access Token (PAT). For help creating a PAT see below.

Once you have your PAT, store the GitHub username and PAT in the local **./app/.env** file.

See the file **./app/env.template** for the required environment variables. To create your own **./app/.env** file, copy **env.template** to **.env** and edit the file.

```text
# Username and Token to use against GitHub
# Do not quote the GitHub values since quotes will be passed into the script!
GITHUB_USERNAME=your-username-here
GITHUB_TOKEN=your-token-here
```

> **Notes:** 
> - The way git stores repo details when accessing via PAT, the PAT is stored in the git config file along with the backup. This means that if you keep the backup in an insecure location, the PAT could be compromised. Therefore, it is recommended that you keep the backup in a secure location.
> - If your PAT changes after you have run the script, you will need to delete the local git repository and re-run the script. This is because the PAT is stored in the git config file, and the script does not currently update the git config file. It is possible to update the git config, but it's not currently supported in this script (see roadmap).

### Creating a Personal Access Token

See [GitHub Docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) for more information.

Note that the PAT you create must have access to the repos you intend to back up, otherwise, not all repos might be accessible, and this might cause the script to fail.

## Running the Backup Script

The backup script is Python3 and can either be run natively or via Docker.

### Running the Backup Script Natively (macOS or Linux)

1. Install Python3. If not already installed, here are some options:
   - macOS use [Homebrew](https://brew.sh/)
   - linux use [The Hitchhiker's Guide to Python](https://docs.python-guide.org/starting/install3/linux/)
2. Inside this repo's "app" directory, set up a virtual Python environment `python3 -m venv venv`. You only need to set up the virtual environment once so long as you've not deleted the "venv" directory.
3. Activate the virtual environment `source venv/bin/activate`
4. Install the required Python packages `pip install -r requirements.txt`
5. Run the backup script 
   ```bash
   $ python3 backup-github.py --org-name="your-org-name" --team-name="your-team-name" --repos-directory="/full/path/to/your/repos/backup/directory"`
   ```

### Running the Backup Script via Docker

1. Install Docker for your OS.
2. From the root of this repo
   - build the Docker image `./x-docker-build.sh` (you only need to do this once so long as you've not deleted the image).
   - Run the backup script
      ```bash
      $ ./x-docker-backup-githup.sh "your-org-name" "your-team-name" "/full/path/to/your/repos/backup/directory"
      ```

**Docker Notes:**
- The script is packaged into the Docker image, therefore, if you make any python script changes, you need to re-build the image.
- The .env file is passed as a volume, so updating credentials does not require rebuilding.

## Restoring a backed-up repository

A backed-up repository can't be used directly in MIRROR mode. Therfore, before you can use it to do work (and have a working copy), you need to restore it to a normal git repository.

### Restoring to a local git repository

1. Create a new directory for the restored repository.
2. Change into the backed-up respiratory directory.
3. `git clone . <new_working_copy_directory>`
4. `cd <new_working_copy_directory>`

You now have a working copy of the repository. Don't forget to set up a remote repository if you intend to push changes back to a remote repository. This remote does not need to be the same as the original repository remote. You can setup a new remote for the restored repository with `git remote set-url origin <new_remote_url>`.

Also, if you have any large files in the repository, and want to use Git LFS, you will need to make sure you have git-lfs installed so that when you push to the new remote, those large files are stored using LFS.

### Restoring to GitHub (or some other hosted Git)

Instructions are based on [GitHub Docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository#mirroring-a-repository).

1. Create a new empty repository on GitHub (or elsewhere).
2. From inside the backup repository folder, run the following commands with the path-to-git of your destination repository:
    ```bash
    git push --mirror [path to git - either ssh or https]
    git config lfs.https://[https path to git]/info/lfs.locksverify true
    git lfs push --all [path to git - either ssh or https]
    ```
   Notes:
   - You must be able to authenticate to the target git repository.  If you are using ssh, you must have your ssh keys set up correctly, or if using a PAT for your new destination, make sure you use an HTTPS url for your repo with username:pat-here@github.com (or whatever git host you're using). Having said that, so long as you can authenticate to your new repository, the above commands should work.
   - When doign the initial push, it's safe to ignore "error: failed to push some refs to 'github.com:your-name/your-repo.git'". This happens when you mirror a GitHub repo that has pull requests made to it. See this [SO answer](https://stackoverflow.com/questions/34265266/remote-rejected-errors-after-mirroring-a-git-repository).

## Roadmap

- Add support for regex matching on repository name (for inclusion and exclusion via individual command line arguments.)
- Add support for updating the git config file with a new PAT? (When a user's PAT changes, the old one stored in the git config file needs to be updated. This means that the user needs to update the config, which is not supported now by the script. An easy workaround is for the user to delete the local git repository and re-run the script with the new PAT.)
  - This might make sense as a separate script, since it's not really part of the backup process, but more so a one-time update. 
- Add a restore script? (This would be a separate script that would take a local backup and restore it to a new GitHub repo. This would be useful for creating a new repo from a backup, or for restoring a repo that was accidentally deleted.)