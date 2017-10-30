#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    production = os.environ.get('PRODUCTION', False)
    staging = os.environ.get('STAGING', False)

    # This should be set depending on the context.
    os.environ['DJANGO_SETTINGS_MODULE'] = 'eval_project.settings'
    if production:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'eval_project.production_settings'
    elif staging:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'eval_project.staging_settings'

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
