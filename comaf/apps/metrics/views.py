from django.shortcuts import render
from django.views.generic import DetailView, ListView
from comaf.apps.base.views import LoginRequiredMixin
import comaf.apps.metrics.models as metrics_models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

class MetricDetailView(DetailView):
    """View for viewing projects"""
    model = metrics_models.Metric
    template_name = 'metric_view.html'

    def get_context_data(self, **kwargs):
        context = super(MetricDetailView, self).get_context_data(**kwargs)
        context['plots'] = context['metric'].get_plots_in_order()
        return context

class MetricListView(ListView):
    """View for viewing projects"""
    #model = metrics_models.Metric
    template_name = 'metric_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = metrics_models.Metric.objects.all()
        #queryset = queryset.filter(owner=self.request.user)
        return queryset

    #def get_context_data(self, **kwargs):
    #    context = super(MetricDetailView, self).get_context_data(**kwargs)
    #    context['plots'] = context['metric'].get_plots_in_order()
    #    return context

class MetricUserListView(ListView):
    """View for viewing projects"""
    #model = metrics_models.Metric
    template_name = 'metric_user_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = metrics_models.Metric.objects.all()
        queryset = queryset.filter(owner__username=self.kwargs['user'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MetricUserListView, self).get_context_data(**kwargs)
        context['current_view_user'] = User.objects.get(username=self.kwargs['user'])
        return context
