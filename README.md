# DJANGO app using google maps api and synchronized google fusion tables.

- Add locations to google fusion table.
- Stores previously pinned locations.
- Display Fusion tables layer with styles applied.
- Personalized Info window for previously searched addresses.

## Usage requirements

Generate a `service_account.json` file from [Service Account Page](https://console.cloud.google.com/iam-admin/serviceaccounts)
and a `client_id.json` file for Oauth 2.0 authentication

Create one [here](https://console.developers.google.com/apis/credentials) and save in project root directroy

Add API keys for [Google Maps API](https://developers.google.com/maps/web/), and [Google Fusion Table REST API](https://developers.google.com/fusiontables/docs/v2/getting_started#about-rest) to `google_api_keys.json`


Also manage API Keys from the [Console](https://console.developers.google.com/apis/credentials)

```json
{
  "maps-api-key": "[[insert map api key]]",
  "fusion-table-api-key": "[[insert fusion table api key]]",
  "client-secret": "[[insert client_id.json client_secret]]"
}
```

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

Create a super user.

```
python3 manage.py createsuperuser
```
OR
`make superuser` from project root folder

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
pip install -e .
pip install -e .[test]`
npm install --only=dev`
python3 manage.py migrate map_app
python3 manage.py migrate static_precompiler
python3 manage.py runserver
```


#### Generate Documentation
```
   cd docs
   make html
```
OR Run in project root
```
    make docs
```

On Windows run

```
    make.bat docs
```



#### View Documentation
```
   cd docs
   sphinx-serve -b build
```
OR
```sh
   make view_docs
```

##### Visit
>  http://localhost:8081

#### Run Test
```
 tox
```
