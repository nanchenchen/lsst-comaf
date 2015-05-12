from django.conf.urls import url

from comaf.apps.api import views

api_root_urls = {
    'metrics': url(r'^metrics/$', views.MetricsView.as_view(), name='metrics'),
}

urlpatterns = api_root_urls.values() + [
    url(r'^$', views.APIRoot.as_view(root_urls=api_root_urls)),
]
