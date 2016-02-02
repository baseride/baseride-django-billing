#
# -- encoding=utf-8

from django.db import models
from json_field import JSONField
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q, F
from django.contrib import auth

PAYMENT_PROFILE_STATUS = (
    ( 'A', _('Active') ),
    ( 'L', _('Locked') ),
    ( 'P', _('Passive') ),
)

class BaseBillingPlan(models.Model):
    name = models.CharField(max_length=128,verbose_name=_('Name'),help_text=_('Name of the billing plan'))
    universal_key = models.CharField(max_length=32,blank=True,null=True,db_index=True,verbose_name=_('Universal key'),help_text=_('Universal key for fast plan search'))
    features = JSONField(verbose_name=_('Features'),help_text=_('Billing plan details'))

    def __unicode__(self):
        return unicode(self.name)


class BasePaymentProfile(models.Model):
    user_profile = models.ForeignKey(auth.models.User,null=True,on_delete=models.SET_NULL,verbose_name=_('User'),help_text=_('User owner'),related_name='payment_profiles')
    status = models.CharField(max_length=2,default='P',choices=PAYMENT_PROFILE_STATUS,verbose_name=_('Status'),help_text=_('Current status of profile'), db_index=True)
    plan = models.ForeignKey(BaseBillingPlan,null=True,on_delete=models.SET_NULL,verbose_name=_('Billing Plan'),help_text=_('Billing Plan'))
    payment_details = JSONField(verbose_name=_('Details'),help_text=_('Payment profile details'))
    creation_ts = models.DateTimeField(auto_now_add=True, help_text='When the profile has been created', verbose_name='Created', db_index=True)

    class Meta:
        verbose_name = _('Payment profile')
        verbose_name_plural = _('Payment profiles')

    def __unicode__(self):
        return unicode('%s (%s) %s' % (self.user_profile.username, self.status, self.plan.name))


class BaseBillingLog(models.Model):
    creation_ts = models.DateTimeField(auto_now_add=True, help_text='When the log entry has been created', verbose_name='Created', db_index=True)
    features = JSONField(verbose_name=_('Features'),help_text=_('Billing details'))
    payment_profile = models.ForeignKey(BasePaymentProfile,verbose_name=_('Payment Profile'),help_text=_('Payment profile'),related_name='profile_logs')

    def __unicode__(self):
        return unicode('%s %s' % (str(self.creation_ts), self.payment_profile.user_profile.username))
