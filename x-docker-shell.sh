#!/bin/bash

# check to ensure that the first argument is a directory and was passed
if [ -z "$1" ] || [ ! -d "$1" ]; then
  echo "Please provide a directory to mount as a volume for the repos!"
  exit 1
fi

# check to ensure that ./app/.env exists
if [ ! -f "./app/.env" ]; then
  echo "Please create the .env file with your GitHub credentials in the app directory!"
  exit 1
fi

# Start a bash shell via docker run, passing in the repos directory as a volume, and the organization
# and team names as arguments.
docker run -it \
  -v ./app/.env:/app/.env \
  -v "$1":/repos/ \
  -w /app \
  backup-github /bin/bash