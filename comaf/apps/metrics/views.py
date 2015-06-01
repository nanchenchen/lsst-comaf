from django.shortcuts import render
from django.views.generic import DetailView
from comaf.apps.base.views import LoginRequiredMixin
import comaf.apps.metrics.models as metrics_models

# Create your views here.

class MetricDetailView(LoginRequiredMixin, DetailView):
    """View for viewing projects"""
    model = metrics_models.Metric
    template_name = 'metric_view.html'

    def get_context_data(self, **kwargs):
        context = super(MetricDetailView, self).get_context_data(**kwargs)
        context['plots'] = context['metric'].get_plots_in_order()
        return context
