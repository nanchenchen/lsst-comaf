from django.contrib import admin
import comaf.apps.metrics.models as metric

# Register your models here.
admin.site.register(metric.Metric)
admin.site.register(metric.Plot)
admin.site.register(metric.Stat)