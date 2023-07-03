#!/bin/bash

# This script will update the Recommendation API. It will stop the recommender service,
# install any new dependencies and restart the Recommendation API.

# Stop recommender service
systemctl stop recommender

# Update the recommendation API
sudo -iu mastodon bash -c 'cd ~/live/scripts && ./update_recommender.sh'
# Check if the update was successful
if [ $? -ne 0 ]; then
    echo "Recommender update failed."
    exit 1
fi

# Start recommender service
systemctl start recommender
# Check if the service started successfully
if [ $? -ne 0 ]; then
    echo "Recommender service failed to start."
    exit 1
fi
