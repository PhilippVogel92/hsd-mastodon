#!/bin/bash

# This script updates the dependencies of the recommendation algorithm.
#
# ** It should be run as the mastodon user. **
# ** It assumes that the Mastodon live server and the recommendation API is stopped before running this. **
# ** It assumes that the recommender is deployed inside of a virtual environment located at /home/mastodon/live/recommender_api/venv. **

set -e # Stop on error

echo "Updating the Recommmender API."

# Updating Python dependencies
pushd /home/mastodon/live/recommender_api
source "./venv/bin/activate"
pip install -r requirements.txt --no-cache-dir
deactivate
popd

echo "Finished updating Recommmender API."
