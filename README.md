# ![Browl](http://i.imgur.com/876ie7H.png) Browl-API [![Build Status](https://travis-ci.org/erkarl/browl-api.png?branch=master)](https://travis-ci.org/erkarl/browl-api)  
Backend for [Browl](https://github.com/erkarl/browl). [Live demo.](http://browl-api.karlranna.com)

## Install 

### Clone, set up virtualenv
Clone this repo, set up and activate a virtualenv:
```console
git clone git@github.com:erkarl/browl-api.git
cd browl-api 
virtualenv env
source env/bin/activate
```

### Setup Database
Create a new PostgreSQL user with the username `browl` and password `browl`. Grant it access to `browl` database.

Optionally, if you'd like to use SQLite3 as your DB backend - just change `DATABASES` setting in `../browl-api/browl/settings.py`:
```console
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```

### Setup Dependencies
```console
make install
make initdb
```

## Run the server 
```console
make server
```
Launch [http://localhost:7000](http://localhost:7000) in your browser.

## Tests 
```console
make test 
```
