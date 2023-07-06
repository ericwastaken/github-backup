FROM alpine:3.18

# Add OS Aliases
# Add the alias to the bash configuration file
RUN echo "alias ll='ls -la'" >> /root/.bashrc

# Bring in bash, git, git-lfs, and openssh-client
RUN apk add --no-cache bash git git-lfs openssh-client
RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

# Install python/pip
# Dependencies also required build tools: python3-dev gcc libc-dev libffi-dev
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 python3-dev gcc libc-dev libffi-dev && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /app

# Copy requirements.txt file
COPY ./app/requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy script files
COPY ./app/modules/* ./modules/
COPY ./app/*.py .
