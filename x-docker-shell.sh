#!/bin/bash

# check to ensure that the first argument is a directory and was passed
if [ -z "$1" ] || [ ! -d "$1" ]; then
  echo "Please provide a directory to mount as a volume for the repos!"
  exit 1
fi

# if we received an additional parameter, use it as SOURCE_ENV_FILE_PATH otherwise,
# set it to the default "./app/.env"
if [ -z "$2" ]; then
  SOURCE_ENV_FILE_PATH="./app/.env"
else
  SOURCE_ENV_FILE_PATH="$2"
fi

SOURCE_REPOS_DIR_PATH="$1"

# check to ensure that ./app/.env exists
if [ ! -f "$SOURCE_ENV_FILE_PATH" ]; then
  echo "Please create the .env file with your GitHub credentials in the app directory!"
  exit 1
fi

# Start a bash shell via docker run, passing in the repos directory as a volume, and the organization
# and team names as arguments.
docker run -it \
  -v "$SOURCE_ENV_FILE_PATH":/app/.env \
  -v "$SOURCE_REPOS_DIR_PATH":/repos/ \
  -w /app \
  backup-github /bin/bash