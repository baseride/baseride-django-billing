#
# -- encoding=utf-8

from django.contrib import admin
from models import *
from django import template


class BaseBillingPlanAdmin(admin.ModelAdmin):
    model = BaseBillingPlan

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(BaseBillingPlanAdmin, self).get_readonly_fields(request, obj)
        return [f.name for f in self.model._meta.fields]

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def get_actions(self, request):
        actions = super(BaseBillingPlanAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions


class BasePaymentProfileAdmin(admin.ModelAdmin):
    model = BasePaymentProfile

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['creation_ts']
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_actions(self, request):
        actions = super(BasePaymentProfileAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions


class BaseBillingLogAdmin(admin.ModelAdmin):
    model = BaseBillingLog

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(BaseBillingLogAdmin, self).get_readonly_fields(request, obj)
        return [f.name for f in self.model._meta.fields]

    def get_actions(self, request):
        actions = super(BaseBillingLogAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

