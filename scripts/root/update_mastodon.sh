#!/bin/bash

# Running this script will update the Mastodon instance to the latest version.
# It will stop Mastodon services, create a backup, update the code, run database
# migrations, and precompile assets. It will then start Mastodon services again.
#
# The script will be run by the deployment pipeline whenever a new commit is pushed to
# the main branch of the repository. It can also be run manually by the root user.
#
# IMPORTANT: This script should be copied to a root-owned directory, e.g. /root/scripts
# and that file should be owned by root and not writable by anyone else to avoid any
# security issues of running untrusted code as root.

# Stop Mastodon services
systemctl stop mastodon-web mastodon-sidekiq mastodon-streaming
# Update Mastodon using a script that will be run as the mastodon user
sudo -iu mastodon bash -c "cd ~mastodon/live/scripts && ./update_live_server.sh"
# Start Mastodon services
systemctl start mastodon-web mastodon-sidekiq mastodon-streaming
