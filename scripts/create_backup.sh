#!/bin/sh

# This script creates an encrypted, compressed and deduplicated backup
# of the Mastodon instance, including the PostgreSQL database, Redis
# database and the Mastodon live instance. It uses Borg Backup to
# create the backup and prune old backups.
#
# A cronjob should be set up to run this script regularly.
# Example crontab entry:
# 0 4 * * * /home/mastodon/live/scripts/create_backup.sh
#
# ** This script should be run as the mastodon user. **
#
# See ProjectBase documentation for more information and recovery instructions:
# https://projectbase.medien.hs-duesseldorf.de/se/hsd-mastodon/-/wikis/Technische-Dokumentation/Automatisierte-Backups

# Backup Mastodon PostgreSQL database to temporary file
pg_dump -Fc mastodon_production > /home/mastodon/.backup-tmp/db.dump

# Export all variables from the .env file
set -a
source .env # Should contain BORG_REPO and BORG_PASSPHRASE
set +a

# some helpers and error handling:
info() { printf "\n%s %s\n\n" "$( date )" "$*" >&2; }
trap 'echo $( date ) Backup interrupted >&2; exit 2' INT TERM

info "Starting backup"

# Backup the most important directories into an archive named after
# the machine this script is currently running on:
# Some directories to exclude from backup because they contain too many unimportant files
borg create                         \
    --verbose                       \
    --filter AME                    \
    --list                          \
    --stats                         \
    --show-rc                       \
    --compression zstd,10           \
    --exclude-caches                \
    --exclude '/home/mastodon/live/node_modules/*' \
    --exclude '/home/mastodon/live/vendor/bundle/*' \
    --exclude '/home/mastodon/live/.rbenv/*' \
    --exclude '/home/mastodon/live/.git/*' \
                                    \
    ::'{hostname}-{now}'            \
    /home/mastodon/live             \
    /home/mastodon/.backup-tmp      \
    /var/lib/redis

# Remove temporary database dump
rm /home/mastodon/.backup-tmp/db.dump

backup_exit=$?

info "Pruning repository"

# Use the `prune` subcommand to maintain 7 daily, 4 weekly and 6 monthly
# archives of THIS machine. The '{hostname}-*' matching is very important to
# limit prune's operation to this machine's archives and not apply to
# other machines' archives also:
borg prune                          \
    --list                          \
    --glob-archives '{hostname}-*'  \
    --show-rc                       \
    --keep-daily    7               \
    --keep-weekly   4               \
    --keep-monthly  6

prune_exit=$?

# use highest exit code as global exit code
global_exit=$(( backup_exit > prune_exit ? backup_exit : prune_exit ))

if [ ${global_exit} -eq 0 ]; then
    info "Backup and Prune finished successfully"
elif [ ${global_exit} -eq 1 ]; then
    info "Backup and Prune finished with warnings"
else
    info "Backup and Prune finished with errors"
fi

exit ${global_exit}
