FROM postgres:15-alpine

COPY ./docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/
# COPY ./init_agweather_db.sql .
# ENTRYPOINT cat init_agweather_db.sql | docker exec -i db psql --user=otekvonsoraden --dbname=agweather_db
# ENTRYPOINT psql --version
# ENTRYPOINT pg_restore -d agweather_db -U otekvonsoraden --no-owner --clean init_agweather_db.sql