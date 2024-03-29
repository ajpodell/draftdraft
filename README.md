# Home of the one and only draftDraft

## Technologies
* Language
  * python
  * flask framework
  
* DB
  * postgres 15
  * ORM: flask-sqlalchemy
  * Migrations: flask-migrate, a wrapper of alembic

* Server
  * gunicorn - version 20.1.0
  * _Note: other options could be flask run or other servers, but no real need right now_

* Frontend
  * flask templates
  * _Note: this is default with flask and is good enough_
  * _Note: could consider react or something in the future


## Getting Started
### Pre reqs
* download python 3.10 to your machine
* download pip (package manager)
  * _Note: honestly not sure how I downloaded this. lots of ways though_
* download postgresql 15
  * desktop version, through homebrew, or docker all work
  * if docker, download docker desktop (https://www.docker.com/products/docker-desktop/)
    * run `docker compose up` to run postgres
    * run `docker compose down` to stop it
    * _Note: see `docker-compose.yaml` file for how that works_
  * if homebrew,
    * run `brew install postgresql@15`
    * run the brew start postgres command, or something like that
    * run `createdb draftdraft` from a psql console

### Running the app
* create a virtual environment 
  * _Note: do this however you want, but I'm using pyenv to activate a venv called draftdraft - Aaron_
    * https://towardsdatascience.com/managing-virtual-environment-with-pyenv-ae6f3fb835f8
    * configure virtual env to alway turn on while in draftdraft `pyenv local draftdraft`
  * _Note: my IDE made one for me and I don't fully get it - Greg_
* install the requirements
  * `python3 -m pip install -r requirements.txt`
* set up .env file
  * create a `.env` file
  * _Note: use `.env.example` as a sample_and replace values with yours
* put the project in your path
  * `python setup.py develop`
  * _Note: I dont fully understand this part - Aaron_
  * _Note: I skipped this for now - Greg_
* set up the tables within the db
  * run `flask db upgrade`
  * _Note: this runs migration files in the migrations directory_
  * Make sure your db is running
* seed players table with real player data and add some users
  * `python ./dev_tools/db_setup.py`[--insert-teams] [--insert-players]
    * for now dont include the flags as theyre both enabled by default and i dont feel like updating
* run the app!
  * `gunicorn --reload --reload_extra_file "templates" "app.create_app()"`
  * I'm managing this command in a `start_app` script. so can just `./start_app`
  * _Note: you could also just hit the python file directly or flask run_
  * _Note: if in an IDE, it'll probably know how to run the app and you can click a button_
 

### DB Migrations
* documentation here:
  * https://flask-migrate.readthedocs.io/en/latest/#command-reference
* for now, since we don't really need migrations, we can keep on editing the initial-migration.py file
* when you make a db change either
  * create a new migration file (and we will just start doing this for all changes)
    * `flask db migrate -m "migration name goes here"` to create the migration file
    * `flask db upgrade` to run it
  * OR (and i'm leaning this way for now) delete the current initial_migration file
    and then recreate it. The framework should auto create the schema for you based on the models, but double check it since it's not always perfect
    * delete the current initial_migration.py file
    * `flask db migrate -m "Initial migration."` to recreate it w/ the changes
    * `flask db upgrade` to run it
* to revert a migration run `flask db downgrade`

------
TODO:
see the github issues for the latest tasks

Project
* dockerize the env
* configs - local/debug - this is started with config.py & .env

Random Issues + Workarounds
* ``` ModuleNotFoundError: No module named 'app'``` when running python scripts
  *  ```export PYTHONPATH=$PATHONPATH:`pwd` ``` was the fix for me. you need to set your PYTHONPATH
