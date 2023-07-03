#!/bin/bash

# Script must be executed as the mastodon user!
# Creates a new account without having to confirm the email
# The generated password is printed at the end of the script
read -p 'Account name (tag, not display name): ' username
read -p 'E-Mail: ' email
RAILS_ENV=production /home/mastodon/live/bin/tootctl accounts create "$username" --email "$email" --confirmed
