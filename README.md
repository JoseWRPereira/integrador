# Project: Integrator

# Workflow

## Create a virtual environment

```python
virtualenv -p python3 env
```


## Enter the virtual environment
```py
source env/bin/activate
```
## Exit the virtual environment
```py
deactivate
```


## Install flask
```py
pip3 install flask
```

## Get requirements
```py
pip3 freeze > requirements.txt
```

## Install requirements
```py
pip3 install -r requirements.txt
```


## Export environment variables
```py
	export FLASK_APP=app
	export FLASK_ENV=development
```