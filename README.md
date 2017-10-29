# [DJANGO app using Google Maps API](https://gogglefusion.herokuapp.com/) for synchronizing data to google fusion tables using OAuth2. 
[![Build Status](https://travis-ci.org/jackton1/django_google_app.svg?branch=master)](https://travis-ci.org/jackton1/django_google_app)
[![Build status](https://ci.appveyor.com/api/projects/status/r713eskuf4qp1uda/branch/master?svg=true)](https://ci.appveyor.com/project/jackton1/django-google-app/branch/master)

- Validate access to google fusion table v2 api using OAuth2.
- Perform updates to google fusion table with locations on the map by clicking or changing the position of the marker on the map. 
- Delete all locations from google fusion by clicking the reset button.
- Stores previously pinned/clicked locations in the fusion table.
- Display Fusion tables layer with styles applied (i.e All locations saved in the fusion table have custom style and description Text Content).
- Personalized Info window for previously searched addresses.

## Usage requirements

Create a `client_id.json` [here](https://console.developers.google.com/apis/credentials) for OAuth v2.0 authentication and save in project root directory.

Add API keys for [Google Maps API](https://developers.google.com/maps/web/), and [Google Fusion Table REST API](https://developers.google.com/fusiontables/docs/v2/getting_started#about-rest) to `google_api_keys.json`


Also manage API Keys from the [Console](https://console.developers.google.com/apis/credentials)

### Sample `google_api_keys.json`
```json
{
  "maps-api-key": "[[insert google map api key]]",
  "fusion-table-api-key": "[[insert google fusion table api key]]",
  "client-secret": "[[insert client_id.json client_secret]]"
}
```

### Create a virtual environment using `virtualenvwrapper`
- Run
```
pip install virtualenv virtualenvwrapper
mkvirtualenv localve
```

### Setup with `virtualenv` 
```
pip install virtualenv
virtualenv localve
```
#### On Windows activate the virtaulenv.
```
localve\Scripts\activate
``` 
#### On Posix system activate the virtualenv
```
source localve/bin/activate
```


### Install the project requirements
```bash
pip3 install -r requirements.txt
npm install
```
### Run migrations
```sh
python3 manage.py migrate
```
### Create a super user to access the application.
```
python3 manage.py createsuperuser
```
##### OR run `make superuser` from project root folder

### Start django web server
```
python3 manage.py runserver
```
OR 
```
make run
```
### Navigate to http://localhost:8000

### Local Development
```bash
git clone https://github.com/jackton1/django_google_app.git
cd django_google_app
pip install -e . -r requirements.txt
npm install 
python3 manage.py migrate 
python3 manage.py runserver
```


#### Generate Documentation
```
cd docs
make html
```
##### OR Run in project root `make docs`

#### View Documentation
```
cd docs
sphinx-serve -b build
```

##### Visit
>  http://localhost:8081

###### OR run `make view_docs` 
> This opens up a browser window with the documentation url http://localhost:8081.

#### Run Test
```
pip install -e .[test]
make test
tox
```
