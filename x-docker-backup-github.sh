#!/bin/bash

# check to ensure the first and second arguments are not empty
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Please provide an organization name and team name!"
  exit 1
fi

# check to ensure that the third argument is a directory and was passed
if [ -z "$3" ] || [ ! -d "$3" ]; then
  echo "Please provide a directory to mount as a volume for the repos!"
  exit 1
fi

# check to ensure that ./app/.env exists
if [ ! -f "./app/.env" ]; then
  echo "Please create the .env file with your GitHub credentials in the app directory!"
  exit 1
fi

# Run the script via docker run, passing in the repos directory as a volume, and the organization
# and team names as arguments.
docker run -i \
  -v ./app/.env:/app/.env \
  -v "$3":/repos/ \
  -w /app \
  backup-github python3 backup-github.py --org-name="$1" --team-name="$2" --repos-directory="/repos/"