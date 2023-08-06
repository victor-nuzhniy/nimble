# nimble api

## Description
    
1. The project created in accordance with test backend task
    https://docs.google.com/document/d/1kal62ycDv548fS0B-eAc4I8E93snzd8PtnNAcDD7BrE/edit?pli=1
2. Django framework was used as a backend creating API.
3. Celery and redis are used for creation updating contacts table once in 24 hours.
4. API for fetching updating data is https://api.nimble.com/api/v1/contacts
5. ORM is not used in the project.
6. Postgress fulltext search is used for fetching data from the table.
7. Fulltext search is implemented with 'websearch_to_tsquery' function. That suppose to
    perform:
        - "alex" - searching for 'alex' in all table contacts fields as a separete word 
             case insensetive;
        - "alex man" searching for 'alex man' combination of words in order they are;
        - "alex or ken" - searching for 'alex' or 'ken' words, both and separate
            in all fields.
        - for more info go https://www.postgresql.org/docs/current/functions-textsearch.html
            "websearch_to_tsquery" function.
8. Search API endpoint is on 'http://localhost:8000/api/contacts/search', request with 
    POST method. Example:
        url = 'http://127.0.0.1:8000/api/contacts/search/'

        response = requests.post(
            url=url,
            headers={"Content-Type": "application/json"},
            json={"search_data": "oleg or ken or kari"}
        )
9. '127.0.0.1:8000' or 'locashost:8000' is used in case of local running. External link
    will be given separately.
10. Given API has its documentation, link 'http://localhost:8000/' in case of local running.
    It has several endpoints for technical usage, some of them can be accessed authorized
    as an admin:
        - '/contacts/' - get all tables contacts, without any authentification;
        - '/contacts/delete/' - delete all contacts, user must be admin;
        - '/contact/create/' - create single contact, user must be admin;
        - '/contact/{int:pk}/' - get and delete contact, user must be admin;
        - '/contact/{int:pk}/update/' - update contact, user must be admin;
        - '/contacts/search/' - search contacts with an input string, without any auth.
11. User registration can be performed in Django 'admin' section.

## Development

1. Create in the project root (or obtain from team member) an `.env` file with 
    environment variables required by application.

### Performing commits

1. Pre-commit hook installed, settings are in .pre-commit-config.yaml
2. To instantiate new hook settings change .pre-commit-config.yaml file
     and run     pre-commit install
3. To bypass hook checking run      git commit -m "..." --no-verify

### Local run in docker container using docker-compose

1. Ensure `.env` file has at least `POSTGRES_USER`, `POSTGRES_PASSWORD` and 
    `POSTGRES_DB` variables set to any string values.
2. Run _postgres_ in docker containers:

       docker-compose up  # run all services defined in docker-compose file

### Setup database using sql files

For work with application, you need to setup your database in docker container. To perform this:

1. While postgres docker container is running, enter it (use separate terminal):

       docker exec -it nimble_contacts bash

2. Enter inside psql terminal (inside your container):

       psql -U postgres

3. Create database for use it in our application and use it (inside psql terminal):

       CREATE DATABASE nimble;
       \c nimble;

4. Change in .env file in root directory value of POSTGRES_DB on nimble

5. Rebuild docker and up it, use commands:

       docker-compose build --no-cache
       docker-compose up

### Redis

1. We will use a celery that's in turn uses Redis. 
    To start a Redis server on port 6379, run the following command:
        docker run -p 6379:6379 -d redis:5

### Celery

1. To run celery use command in terminal
    celery -A config worker -l -P solo (-P solo for Windows)
2. To run beat service use command in terminal
    celery -A config beat
3. To upgrade celery settings run
    celery upgrade settings config/settings.py
4. To delete task from the queue
    celery -A config purge

### Load data into contacts from csv file.

1. To load data from csv file to contacts table, use command

    python manage.py import_contacts_from_csv data/nimble_contacts.csv
    
    where last argument is a csv file location.



### Performing tests

For testing application there is need to use pytest and it's plugings.
There is need to always check amount of test cases and their covering.

1. To perform created test cases, use command:

       pytest --cov