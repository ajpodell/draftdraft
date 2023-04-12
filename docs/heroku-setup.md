## Heroku
- Our app is deployed on Heroku. To deploy and interact with the-draft-draft app, follow instructions below

### Set Up
- Download Heroku CLI (https://devcenter.heroku.com/articles/heroku-cli)
- run `heroku login` to login to CLI
- run `heroku git:remote -a the-draft-draft` to set the Heroku env as a remote repo

### Deploying Code
- run `git push heroku main` to push main to heroku
- run `git push heroku {branch_name}:master` to deploy a specific branch to heroku
- run `heroku logs tail` to tail the logs

### Postgres
- run `heroku run flask db upgrade` to run db migrations
- run `heroku run python dev_tools/player_scraper.py` to seed player data
- run `heroku pg:psql postgresql-defined-81660 --app the-draft-draft` to open a postgres console
  - when querying tables, you will likely need to put 'public' before the table name
    - ex) `select * from public.user`
- see the `SQLALCHEMY_DATABASE_URI` env var for how the app and db are configured
