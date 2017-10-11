from distutils.core import setup

from setuptools import find_packages

setup(
    name='django_map_app',
    version='1.0.0',
    author='Tonye Jack',
    author_email='jtonye@ymail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/jackton1/django_google_app.git',
    license='MIT refer to LICENSE',
    description='Add address with google maps api.',
    long_description=open('README.md').read(),
    zip_safe=False
)
