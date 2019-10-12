# crm-flask

Projeto sobre CRM em Flask.

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/crm-flask.git
cd crm-flask
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=crm
export FLASK_ENV=development

flask db init
flask db migrate -m "customers table"
flask db upgrade

cd crm
flask run
```

Em outro terminal, faça:

```
# Ative a virtualenv
pip install httpie
http POST http://localhost:5000/api/customers name='Abel'
http POST http://localhost:5000/api/customers name='Regis'
http GET http://localhost:5000/api/customers
http PUT http://localhost:5000/api/customers/1 "name=John"
http GET http://localhost:5000/api/customers
```
