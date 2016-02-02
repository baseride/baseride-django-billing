#
# -- encoding=utf-8
from django.db import models, connection
from django.db.models import Q, F
from django.core import validators
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _

import datetime

from baseride_django_billing.core import products

class Command(BaseCommand):
    help = "Calculate all payment profiles"
    def handle(self, *args, **options):

        profiles = models.BasePaymentProfile.objects.filter(status='A')
        print "Start calculate %d profiles..." % len(profiles)
        res = products.calculate_profiles(profiles)
        ln = 0
        for profile in res:
            models.BaseBillingLog.objects.create(payment_profile=profile['profile'], features=profile['features'])
            ln += 1
        print "DONE: %d logs created" % ln
