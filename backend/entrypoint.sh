#!/bin/sh

echo "test"

# if [ "$DATABASE" = "postgres" ]
# then
#     echo "Waiting for postgres..."

#     while ! nc -z $SQL_HOST $SQL_PORT; do
#       sleep 0.1
#     done

#     echo "PostgreSQL started"
# fi

# python manage.py flush --no-input
# python manage.py loaddata test_db.json
# python datascraper/restore_database.py
python -c 'from datascraper.restore_database import restore_from_yandex_disk; print (restore_from_yandex_disk())'

exec "$@"