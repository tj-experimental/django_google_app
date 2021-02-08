from setuptools import setup, find_packages
"""
Django application using google fusion table REST API
"""

install_requires = [
    'Django==1.11.23',
    'google-api-python-client==1.6.4',
    'django-easy-maps==0.9.3',
    'django-appconf==1.0.2',
    'django-classy-tags==0.8.0',
    'django-pipeline==1.6.9',
    'django-static-precompiler==1.8.2',
    'django-tables2==1.11.0',
    'future==0.16.0',
    'futures==3.1.1',
    'geopy==1.11.0',
    'httplib2==0.19.0',
    'jsmin==2.2.2',
    'oauth2client==3.0.0',
    'pyasn1==0.3.7',
    'pyasn1-modules==0.1.4',
    'pytz==2017.2',
    'rsa==3.4.2',
    'six==1.11.0',
    'uritemplate==3.0.0',
    'gcloud',
    'gunicorn==19.7.1',
    'dj-database-url==0.4.2',
    'whitenoise==3.3.1',
    'django-registration-redux==1.8',
    'alabaster==0.7.10',
    'Babel==2.5.1',
    'beautifulsoup4==4.6.0',
    'certifi==2017.7.27.1',
    'chardet==3.0.4',
    'click==6.7',
    'psycopg2==2.7.3.2',
    'colorama==0.3.9',
    'jsonpickle==0.9.5',
    'repoze.lru==0.7',
    'django-bootstrap-breadcrumbs==0.8.2',
]

test_requires = [
    'tox>=2.9.1',
    'coverage',
    'mock==2.0.0',
]

doc_requires = [
    'sphinx==2.1.2',
    'sphinx-serve==1.0.1',
    'recommonmark==0.5.0',
]

lint_requires = [
    'flake8',
    'autopep8',
]

extras_require = {
    'test': test_requires,
    'docs': doc_requires,
    'lint': lint_requires,
}

setup(
    name='django_map_app',
    version='1.0.2',
    author='Tonye Jack',
    author_email='jtonye@ymail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require=extras_require,
    url='https://github.com/jackton1/django_google_app.git',
    license='MIT refer to LICENSE',
    description='Add address with google maps api.',
    long_description=open('README.md').read(),
    zip_safe=False
)
