from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'comaf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
