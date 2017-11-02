from __future__ import absolute_import

import logging

from django.test.runner import DiscoverRunner


class DisableLoggingTestRunner(DiscoverRunner):
    """
    Disable the test runner log level below `logging.CRITICAL`.
    """
    def run_tests(self, *args, **kwargs):
        # Disable logging below critical
        logging.disable(logging.CRITICAL)
        super(DisableLoggingTestRunner,
              self).run_tests(*args, **kwargs)
