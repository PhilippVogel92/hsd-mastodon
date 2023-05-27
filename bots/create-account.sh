#!/bin/bash

# Creates a new account without having to confirm the email
# The generated password is printed at the end of the script
read -p 'Account name (tag, not display name): ' username
read -p 'E-Mail: ' email
sudo -iu mastodon
cd /home/mastodon/live
RAILS_ENV=production bin/tootctl accounts create "$username" --email "$email" --confirmed
exit