# README #

This README would normally document whatever steps are necessary to get your application up and running.

## Configuration

### chromeless
Install https://pypi.org/project/chromeless/ and configure chromeless in aws lambda. by defaul a lambda name is chromeless-server-prod

* Add Lambda Enviroment variable TZ=America/Bogota

### zappa deploy dev
zappa deploy dev


Add envars
* ALLOWED_HOSTS
* BUCKET_FILES
* DATABASE_HOST
* DATABASE_NAME
* DATABASE_PASSWORD
* DATABASE_PORT
* DATABASE_USER
* ENVIRONMENT = production
* SENTRY_URL

