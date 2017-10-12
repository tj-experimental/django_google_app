from distutils.core import setup

from setuptools import find_packages


install_requires = [
    'Django==1.9',
    'google-api-python-client==1.6.4',
    'django-easy-maps==0.9.3',
    'django-easy-maps==0.9.3',
    'django-appconf==1.0.2',
    'django-classy-tags==0.8.0',
    'django-pipeline==1.6.9',
    'django-static-precompiler==1.6',
    'django-tables2==1.11.0',
    'future==0.16.0',
    'futures==3.1.1',
    'geopy==1.11.0',
    'httplib2==0.10.3',
    'jsmin==2.2.2',
    'oauth2client==4.1.2',
    'pyasn1==0.3.7',
    'pyasn1-modules==0.1.4',
    'pytz==2017.2',
    'rsa==3.4.2',
    'six==1.11.0',
    'uritemplate==3.0.0',
    'gcloud',
    'jsonpickle==0.9.5',
    'django-bootstrap-breadcrumbs==0.8.2',
]

test_requires = [
    'tox>=2.9.1',
]

doc_requires = [
    'sphinx==1.6.4',
    'sphinx-serve==1.0.1',
]

extras_require = {
    'test': test_requires,
    'docs': doc_requires,
}

setup(
    name='django_map_app',
    version='1.0.0',
    author='Tonye Jack',
    author_email='jtonye@ymail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    url='https://github.com/jackton1/django_google_app.git',
    license='MIT refer to LICENSE',
    description='Add address with google maps api.',
    long_description=open('README.md').read(),
    zip_safe=False
)
