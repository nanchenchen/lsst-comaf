from django.contrib import admin
import comaf.apps.workspace.models as workplace

# Register your models here.
admin.site.register(workplace.SpaceView)
admin.site.register(workplace.MemberSpace)
admin.site.register(workplace.WorkSpace)