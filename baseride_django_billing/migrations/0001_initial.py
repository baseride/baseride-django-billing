# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseBillingLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_ts', models.DateTimeField(auto_now_add=True, help_text=b'When the log entry has been created', verbose_name=b'Created', db_index=True)),
                ('features', jsonfield.fields.JSONField(default='null', help_text='Billing details', verbose_name='Features')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BaseBillingPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of the billing plan', max_length=128, verbose_name='Name')),
                ('universal_key', models.CharField(max_length=32, blank=True, help_text='Universal key for fast plan search', null=True, verbose_name='Universal key', db_index=True)),
                ('features', jsonfield.fields.JSONField(default='null', help_text='Billing plan details', verbose_name='Features')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BasePaymentProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'P', choices=[(b'A', 'Active'), (b'L', 'Locked'), (b'P', 'Passive')], max_length=2, help_text='Current status of profile', verbose_name='Status', db_index=True)),
                ('payment_details', jsonfield.fields.JSONField(default='null', help_text='Payment profile details', verbose_name='Details')),
                ('creation_ts', models.DateTimeField(auto_now_add=True, help_text=b'When the profile has been created', verbose_name=b'Created', db_index=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Billing Plan', to='baseride_django_billing.BaseBillingPlan', help_text='Billing Plan', null=True)),
                ('user_profile', models.ForeignKey(related_name='payment_profiles', on_delete=django.db.models.deletion.SET_NULL, verbose_name='User', to=settings.AUTH_USER_MODEL, help_text='User owner', null=True)),
            ],
            options={
                'verbose_name': 'Payment profile',
                'verbose_name_plural': 'Payment profiles',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='basebillinglog',
            name='payment_profile',
            field=models.ForeignKey(related_name='profile_logs', verbose_name='Payment Profile', to='baseride_django_billing.BasePaymentProfile', help_text='Payment profile'),
            preserve_default=True,
        ),
    ]
