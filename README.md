.title Home of the draft draft


current thoughts:
* postgres - maybe try free tier on fly.io
* backend - flask, deployed to heroku
* frontend - maybe react native? or webpage? 



Aaron - you came back and forgot this:
* running with `gunicorn --reload --reload_extra_file "templates" app:app`
* port 8000 worked, but 5000 did not (but maybe you just fucked it up)
* you are using pyenv to manage your virtual environment
* you named the pyenv draftdraft and you activate it with `pyenv activate draftdraft` from inside draftdraft/server

technologies
* postgres 15
* python (i have 3.10)
* gunicorn - version 20.1.0
* react? -- not yet



TODO:
Project
* set up tables + alembic?
* login? (later)
* dockerize the env
* actually learn markdown
* autoenv? -- auto move to virtualenv when entering a directory
* configs - local/debug - will circle back when looking to deploy or do anything outside of debug mode


Jan 15
* considering moving away from client & server and using flask templates - will be giving this a shot
* following this: https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application

Jan 12
- trying to set up a local db -- db_setup.py is functional
- not using alembic - just flask_sqlalchemy. thats enough for right now.


.h3 Getting Going
# all of this is assumed to be done from within the `server` directory

# create a virtual environment
## do this however you want, but I'm using pyenv to activate a venv called draftdraft

# install the requirements
python3 -m pip install -r requirements.txt

# install postgres
## brew install postgresql@15
## createdb draftdraft

# put the project in your path. (I dont fully understand this part)
## python setup.py develop

# set up the tables within the db
## ./db_setup.py 


