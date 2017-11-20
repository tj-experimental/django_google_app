from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = ('Updates settings.SITE_ID using the site name specified in '
           'settings.SITE_NAME and settings.SITE_DOMAIN')

    def handle(self, *args, **options):
        current_site = Site.objects.get_or_create(
            name=settings.SITE_NAME,
            domain=settings.SITE_DOMAIN)
        site, exists = current_site
        if not exists or settings.SITE_ID != site.id:
            settings.SITE_ID = site.id
            self.stdout.write(
                self.style.SUCCESS('Successfully updated the settings.SITE_ID'
                                   ' to {}: {}, {}'.format(site.id, site.name,
                                                          site.domain))
            )
        else:
            self.stdout.write(
                self.style.WARNING('Couldn\'t change the settings.SITE_ID '
                                   'to {}: {}'.format(settings.SITE_ID, site.name))
            )