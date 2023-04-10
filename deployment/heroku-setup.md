## Heroku
- Download Heroku CLI (https://devcenter.heroku.com/articles/heroku-cli)
- run `heroku login` to login to CLI
- run `heroku git:remote -a the-draft-draft` to set the Heroku env as a remote repo
- run `git push heroku main` to push main to heroku
  - or is it `git push heroku heroku-deployment(local branch name):master`
- run `heroku logs tail` to tail the logs