#
# -- encoding=utf-8

from django.utils.translation import gettext, ugettext_lazy as _
import datetime
from decimal import *

BILLING_RESOURCES = (
    ( 'T', _('Time of using (days)') ),
    ( 'U', _('Number of users') ),
)

def billing_profile_days(payment_profile, sub_kind):
    if 'period' in sub_kind.keys():
        days = (datetime.date.today() - payment_profile.creation_ts.date()).days
        return days
    return 0


def calculate_feature_cost(feature, value):
    if not isinstance(feature, dict): return Decimal(0)
    if not 'fixed' in feature.keys():
        return Decimal(0)
    if not 'price' in feature['fixed'].keys() or not 'number' in feature['fixed'].keys():
        return Decimal(0)
    cost = Decimal(feature['fixed']['price'])
    value -= int(feature['fixed']['number'])
    if value>0 and 'additional' in feature.keys() and 'price' in feature['additional'].keys() and \
       'every' in feature['additional'].keys() and int(feature['additional']['every'])>0:
        cost += Decimal(feature['additional']['price']) * Decimal(value) / Decimal(feature['additional']['every'])
    return cost


def calculate_profiles(profiles):
    res = []
    for profile in profiles:
        if not 'features' in profile.plan.features.keys(): continue
        fs = []
        for feature in profile.plan.features['features']:
            if not 'kind' in feature.keys(): continue
            if feature['kind'] == 'T':
                value = (datetime.date.today() - profile.creation_ts.date()).days
            else:
                continue
            r = calculate_feature_cost(feature, value)
            fs.append( {'kind':feature['kind'], 'value':value} )
        res.append({ 'profile':profile, 'features':fs })
    return res


def test_user_lock(profile):
    if not 'kind' in profile.plan.features.keys() or not 'period' in profile.plan.features['kind'].keys() or \
        profile.plan.features['kind']['period'] != 'static': return
    days = billing_profile_days(profile, profile.plan.features['kind'])
    if days <= int(profile.plan.features['kind']['duration']): return

    profile.status = 'L'
    profile.save()
