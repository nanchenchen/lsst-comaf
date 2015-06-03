from django.conf.urls import url

from comaf.apps.api import views

api_root_urls = {
    'metrics': url(r'^metrics/$', views.MetricsView.as_view({'get': 'list'}), name='metrics'),
    'plots': url(r'^plots/$', views.PlotView.as_view(), name='plots'),
    'comments': url(r'^metrics/(?P<metric_id>[0-9]+)/comments/$', views.CommentView.as_view(), name='comments'),
}

urlpatterns = api_root_urls.values() + [
    url(r'^$', views.APIRoot.as_view(root_urls=api_root_urls)),
]
