from django.db import models
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

app_label = 'app_settings'

class AppSetting(models.Model):
    app_label = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, default="")

    _type_register = []

    @staticmethod
    def register(app_label, setting_type, setting_name, default=None):
        if setting_type in AppSetting._type_register:
            pass
        else:
            AppSetting._type_register.append(setting_type)
        if default is None:
            obj, is_new = setting_type.objects.get_or_create(app_label=app_label, name=setting_name)
        else:
            try:
                obj, is_new = setting_type.objects.get_or_create(app_label=app_label,
                                              name=setting_name, value=default)
            except IntegrityError:
                obj = setting_type.objects.get(app_label=app_label, name=setting_name)
                is_new = False

        return obj
    @staticmethod
    def get_setting(app_label, setting_name):
        for t in AppSetting._type_register:
            try:
                return t.objects.get(app_label=app_label,
                                     name=setting_name).value
            except t.DoesNotExist:
                pass
        raise ObjectDoesNotExist('Setting not registered: %s - %s' % (app_label,
                                                              setting_name))

    def __str__(self):
        return "%s: %s" % ( self.name, str(self.value))
    class Meta:
        abstract = True
        unique_together = ['app_label', 'name']
        app_label = app_label

class IntegerSetting(AppSetting):
    value = models.IntegerField(default=0)
    class Meta:
        app_label = app_label

class FloatSetting(AppSetting):
    value = models.FloatField(default=0.0)
    class Meta:
        app_label = app_label

class EmailSetting(AppSetting):
    value = models.EmailField(default="example@example.de")
    class Meta:
        app_label = app_label

class BooleanSetting(AppSetting):
    value = models.BooleanField(default=False)
    class Meta:
        app_label = app_label

class StringSetting(AppSetting):
    class Meta:
        app_label = app_label
    pass

class DateSetting(AppSetting):
    value = models.DateField(default=timezone.now)
    class Meta:
        app_label = app_label

class DateTimeSetting(AppSetting):
    value = models.DateTimeField(default=timezone.now)
    class Meta:
        app_label = app_label

