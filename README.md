# DJANGO APP using google maps api. 

## Run

### Requires `virtualenv` and `virtualenvwrapper`

```sh
mkvirtualenv test
pip3 install -r requirements.txt
npm install
python3 manage.py migrate map_app
python3 manage.py migrate static_precompiler
python3 manage.py runserver
```


### Navigate to `localhost` server listens on port `8000`

> http://localhost:8000

### Local Development
```
git clone https://github.com/jackton1/django_google_app.git
cd django_google_app`
pip install -r requirements.txt`
npm install --only=dev`
python3 manage.py migrate map_app
python3 manage.py migrate static_precompiler
```
