# Projeto  Integrador

Hospedagem (Heroku): https://integrado.herokuapp.com/


# Árvore do projeto
```
---\integrador
    '---\app
    '    '---\api
    '    '---\db
    '    '---\equipment
    '    '---\scheduling
    '    '---\static
    '    '---\templates
    '    '---\users
    '    '---app.py
    '
    '---config.py
    '---Procfile
    '---README.md
    '---requirements.txt
    '---wsgi.py
```


# Baixando e rodando a aplicação



```python
###
### No Terminal (git-bash, bash, etc)
###

### Clonar projeto 
git clone https://github.com/JoseWRPereira/integrador.git

### Acessar o projeto
cd integrador

### Instalar o ambiente virtual (virtualenv)
virtualenv -p python3 env

## Ativar o ambiente virtual 
source env/bin/activate


## Instalar requisitos 
pip3 install -r requirements.txt


## Executar o App
flask run

###
### No navegador
###

## Acessar
localhost:5000

## Usar o app

## Administrador
Login: admin@email.com
Senha: admin


###
### No terminal
###

## Saindo da execução do App
<CTRL+C>

## Sair do ambiente virtual
deactivate
```



### Instalando do zero

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


## Implementar (*Deploy*) utilizando Heroku Git

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



## Referências

* Front-end (HTML/CSS): [CodingLab](https://youtu.be/-qWySnuoaTM)

* Ferramenta de validação do HTML: [W3C Markup Validation Service](https://validator.w3.org/)


* Banco de dados: [POSTGRESQL](https://www.postgresqltutorial.com/postgresql-cheat-sheet/)

* Framework web: [Flask doc](https://flask.palletsprojects.com/en/2.1.x/), [Curso de Flask com Julia Rizza](https://youtu.be/r40pC9kyoj0)

* Arquitetura de Projetos Flask: [Henrique Guazzelli Mendes](https://youtu.be/EML_F6W_zrU), [Code Show (Bruno Rocha)](https://youtu.be/-qWySnuoaTM), [Real Python - Use a Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/)

