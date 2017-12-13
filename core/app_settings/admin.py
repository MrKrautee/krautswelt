from django.contrib import admin
from django.urls import reverse

# Register your models here.
from .models import AppSetting, EmailSetting, StringSetting
from .models import IntegerSetting
from .models import FloatSetting
from .models import DateSetting
from .models import DateTimeSetting
from .models import BooleanSetting

def app_index(response):
    type_list = ( EmailSetting, StringSetting, IntegerSetting, FloatSetting,
                 DateSetting, DateTimeSetting, BooleanSetting, )
    values = []
    def mk_value_list(qs):
        for q in qs:
            app_label = q._meta.app_label
            model_name = q._meta.model_name
            link = reverse("admin:%s_%s_change" % (app_label, model_name),
                           args=(q.id,))
            values.append({'app_label':q.app_label, 'name':q.name, 'value':q.value, 'link': link })

    for t in type_list:
        mk_value_list(t.objects.all())
    #sort by name
    values = sorted(values, key=lambda k: k['name'])
    return {'test': "app settings test", 'settings': values}

try:
    from core.advanced_admin.admin import admin_site
    admin_site.register_app_index_extra('app_settings', app_index)
except Exception:
    pass

class EmailSettingAdmin(admin.ModelAdmin):
    pass

admin.site.register(StringSetting, admin.ModelAdmin)
admin.site.register(IntegerSetting, admin.ModelAdmin)
admin.site.register(FloatSetting, admin.ModelAdmin)
admin.site.register(DateSetting, admin.ModelAdmin)
admin.site.register(DateTimeSetting, admin.ModelAdmin)
admin.site.register(BooleanSetting, admin.ModelAdmin)
admin.site.register(EmailSetting, EmailSettingAdmin)

