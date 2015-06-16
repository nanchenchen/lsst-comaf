from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'comaf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='/metric/')),
    url(r'^', include('apps.base.urls')),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^metric/', include('apps.metrics.urls')),
    # REST Api urls
    url(r'^api/', include('apps.api.urls')),

)
