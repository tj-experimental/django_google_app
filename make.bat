@ECHO OFF

set HERE=.\

pushd %~dp0

if -%MANAGEPY%-==-- (
    set PYTHON=python
	set MANAGEPY=manage.py
)

if not -%1-==-- (
    REM calling %1 with args %2 %3
    call :%1 %2 %3
    exit /b
) else (
    goto help
)

:help
echo.
echo.Available commands ^for project
echo."make clean-pyc" Remove python compiled files.
echo."make run" Spin up django server
echo."make test" Run Test
echo."make tox_test" Run tox locally
echo."make collectstatic" Collect static files in project.
echo."make superuser" Creates a super user.
echo."make clean-build" Clean build Assets.
echo."make lint" Run flake8 /for project files.
echo."make docs" Update the docs and spin up sphinx server.
echo."make install" Install project in editable mode.
exit /b

goto end

:manage
python manage.py %*
exit /b

:test
echo. Running test
call :manage test
echo. Completed running test
exit /b

:migrate
echo. Starting migration
call :manage makemigrations
echo. Ended Migration
echo. Starting Migrate
call :manage migrate
echo.Completed migrate
exit /b

:collectstatic
echo.Collecting Static files.
call :manage collectstatic
echo.Completed collecting static files
exit /b

:run
setlocal EnableDelayedExpansion
if -%HOST%-==-- (
   set HOST=127.0.0.1
)
if -%HOSTNAME%-==-- (
    set HOSTNAME=localhost
)
if -%PORT%-==-- (
    set PORT=8000
) else (
    REM set this 2 raised to power 16 -1 = 65535
    set /a MAX_PORT=65536 -1
    if !PORT! gtr !MAX_PORT! (
        echo. Invalid Server PORT !PORT! should be less than !MAX_PORT!.
        echo. Modify the PORT env e.g 'set PORT=8000'
        exit /b
    )
)
echo.Starting server on !HOST!^:!PORT!
start chrome.exe !HOSTNAME!^:!PORT!
call :manage runserver !HOST!^:!PORT!
exit /b

:app
echo.Creating app %2
call :manage startapp %2
exit /b

:superuser
call :manage createsuperuser
exit /b

:clean-pyc
find . -name "*.pyc" -exec rm --force {}
exit /b

:clean-build
rm --force -r .\*.egg-info
rm --force -r dist\
rm --force -r build\
exit /b

:lint
flake --exclude=.tox --include=*.py
exit /b

:install
pip install -e . -r requirements.txt
exit /b

:test_install
pip install -e .[test]
exit /b

:doc_install
pip install -e .[doc]
exit /b

:docs
echo.%~dp0docs
cd docs
make.bat html -b build
exit /b

:view_docs
echo.Serving sphinx docs
call :doc_install
call :docs
cd docs
start chrome.exe localhost:8899
sphinx-serve -b build -p 8899

:end
popd
