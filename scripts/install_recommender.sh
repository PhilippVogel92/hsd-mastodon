#!/bin/bash

# This script installs the Recommender API locally. You still need to add the systemd unit file (dist/recommender.service)
# and alter the nginx configuration.

# If there is an error, stop execution.
set -e

echo "Installing Recommender API..."

# 1. Change directory
pushd /home/mastodon/live/recommender_api

# 2. Create a virtual environment (see https://docs.python.org/3/library/venv.html)
python3 -m venv venv

# 3. Activate the virtual environment
source "./venv/bin/activate"

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install Gunicorn (WSGI server)
pip install gunicorn

# 6. Deactivate virtual environment
deactivate

# 7. Leave directory
popd

echo 'The Recommender API has been installed successfully. You still have to change your nginx configuration! You also might want to install and enable the systemd service file (dist/recommender.service).'
