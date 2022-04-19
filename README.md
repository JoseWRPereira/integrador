# Project: Integrator

Hospedagem (Heroku): https://integrado.herokuapp.com/

# Workflow

```python
### Install virtual env
virtualenv -p python3 env

## Enter the virtual environment
source env/bin/activate

## Install flask
pip3 install flask

## Install servidor HTTP Python Web Server Gateway Interface
pip3 install gunicorn

## Get requirements
pip3 freeze > requirements.txt

## Install requirements
pip3 install -r requirements.txt

## Export environment variables
export FLASK_APP=app
export FLASK_ENV=development

## Run App
flask run

## Quit App
<CTRL+C>

## Exit the virtual environment
deactivate
```


## Deploy using Heroku Git

``` bash
## Login
$ heroku login

## Clone the repository
$ heroku git:clone -a integrado 
$ cd integrado

## Deploy changes
$ git add .
$ git commit -am "comment..."
$ git push heroku main
```

## Validate

Tool for check the html markup lenguage: [W3C Markup Validation Service](https://validator.w3.org/)