# [DJANGO app using Google Maps API](https://googlefusion.herokuapp.com/) for synchronizing data to google fusion tables using OAuth2. 
[![Build Status](https://travis-ci.org/jackton1/django_google_app.svg?branch=master)](https://travis-ci.org/jackton1/django_google_app)
[![Build status](https://ci.appveyor.com/api/projects/status/r713eskuf4qp1uda/branch/master?svg=true)](https://ci.appveyor.com/project/jackton1/django-google-app/branch/master)

.. inclusion-marker-do-not-remove

- Validate access to google fusion table v2 api using OAuth2.
- Perform updates to google fusion table with locations on the map by clicking or changing the position of the marker on the map. 
- Delete all locations from google fusion by clicking the reset button.
- Stores previously pinned/clicked locations in the fusion table.
- Display Fusion tables layer with styles applied (i.e All locations saved in the fusion table have custom style and description Text Content).
- Personalized Info window for previously searched addresses.

## Setup requirements

### Generate a OAuth `client_id.json` [here](https://console.developers.google.com/apis/credentials).

- click `Create credentials`.
- select `OAuth client ID`.
- click on the client ID name to modify the restrictions. 
- add the Authorized JavaScript origins e.g `http://localhost:8000`
- add Authorized redirect URIs e.g `http://localhost:8000/oauth2callback`
- click download json.

Using the downloaded json file.
- rename the file to `client_id.json`.
- replace `client_id.json` in project root.

OR

Using the json file copy and set env variables
- `CLIENT_ID` , `PROJECT_ID`, `CLIENT_SECRET`.


### Manage API Keys from the [Console](https://console.developers.google.com/apis/credentials)

#### Generate an API key [here](https://console.developers.google.com/apis/credentials) for [Google Maps API](https://developers.google.com/maps/web/), and [Google Fusion Table REST API](https://developers.google.com/fusiontables/docs/v2/getting_started#about-rest) to keep track of usage information.

##### Create `google_api_keys.json` to store the api keys.
```json
{
  "maps-api-key": "[[insert google map api key]]",
  "fusion-table-api-key": "[[insert google fusion table api key]]"
}
```
##### OR Optionally set ENV vars 

```
EASY_MAPS_GOOGLE_MAPS_API_KEY=

GOOGLE_FUSION_TABLE_API_KEY=
```


### Create a virtual environment using `virtualenvwrapper`
- Run
```
pip install virtualenvwrapper
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
### Start web server
```
python3 manage.py runserver
```
### OR 
```
make run
```

### Navigate to http://localhost:8000




## Local Development
```bash
git clone https://github.com/jackton1/django_google_app.git
cd django_google_app
pip install -e . -r requirements.txt
npm install 
python3 manage.py migrate 
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
