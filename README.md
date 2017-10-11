# DJANGO APP using google maps api. 


### Project requires `virtualenv` and `virtualenvwrapper`
- Run
```
pip install virtualenv virtualenvwrapper
```

### Installation
```bash
mkvirtualenv test
pip3 install -r requirements.txt
npm install
```

### Run migrations
```sh
python3 manage.py migrate map_app
python3 manage.py migrate static_precompiler
```

### Start django web server
```
python3 manage.py runserver
```


### Navigate to `localhost` server listens on port `8000`

> http://localhost:8000

### Local Development
```bash
git clone https://github.com/jackton1/django_google_app.git
cd django_google_app`
pip install -r requirements.txt`
npm install --only=dev`
python3 manage.py migrate map_app
python3 manage.py migrate static_precompiler
```


#### Generate Documentation
```
   cd docs
   make html
```

#### View Documentation
```sh
   cd docs
   sphinx-serve -b build
```

##### Visit
>  http://localhost:8081

#### Run Test
```
 tox
```
