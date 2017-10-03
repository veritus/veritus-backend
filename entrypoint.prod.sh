# Prepend environment variables so that cron can use them
env | sed 's/^\(.*\)$/\1/g' | cat - /tmp/crons > /etc/cron.d/crontab
# Run cron daemon
cron
# Migrate, loaddata and run gunicorn
python3 src/manage.py migrate
python3 src/manage.py loaddata init_data.json
cd src
gunicorn -b 0.0.0.0:80 politech_backend.wsgi
