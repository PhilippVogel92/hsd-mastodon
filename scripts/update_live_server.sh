#!/bin/bash

# This script updates the Mastodon live server to the latest version of the
# ProjectBase repository by pulling from the remote repository. It also creates
# a backup of the Mastodon files and database before updating. After the update,
# database migrations and asset precompilation are run to cover most update
# scenarios. See https://github.com/mastodon/mastodon/releases for additional
# update steps that may be required for specific versions.
#
# ** It should be run as the mastodon user. **
# ** It assumes that the Mastodon live server is stopped before running this. **

set -e # Stop on error

# Load Ruby environment
export RAILS_ENV=production
export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"

echo "Creating backup of Mastodon server..."

# Create backup of Mastodon files and database
/home/mastodon/live/scripts/create_backup.sh

echo "Updating Mastodon server..."

# Update Mastodon files and run database migrations and asset precompilation
pushd /home/mastodon/live
git pull origin
bundle install -j$(getconf _NPROCESSORS_ONLN)
yarn install --pure-lockfile
bundle exec rails db:migrate
bundle exec rails assets:precompile
popd

echo "Finished updating Mastodon server."
