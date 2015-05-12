"""
The view classes below define the API endpoints.

"""

from rest_framework import status
from rest_framework.views import APIView, Response
from django.core.urlresolvers import NoReverseMatch
from rest_framework.reverse import reverse
from rest_framework.compat import get_resolver_match, OrderedDict

import comaf.apps.metrics.models as metrics_models
from comaf.apps.api import serializers

import logging

logger = logging.getLogger(__name__)

class MetricsView(APIView):

    def get(self, request, format=None):
        metrics = metrics_models.Metric.objects.all()
        output = serializers.MetricsSerializer(metrics)
        return Response(output.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        input = serializers.MetricUploadSerializer(data=request.data)
        if input.is_valid():
            parsed_data = input.validated_data
            metrics_models.create_from_post(parsed_data["key"], parsed_data["data"])
            return Response(parsed_data["data"], status=status.HTTP_200_OK)
        return Response(input.errors, status=status.HTTP_400_BAD_REQUEST)

class APIRoot(APIView):
    """
    The Collaborative Maf Root API View.
    """
    root_urls = {}

    def get(self, request, *args, **kwargs):
        ret = OrderedDict()
        namespace = get_resolver_match(request).namespace
        for key, urlconf in self.root_urls.iteritems():
            url_name = urlconf.name
            if namespace:
                url_name = namespace + ':' + url_name
            try:
                ret[key] = reverse(
                    url_name,
                    request=request,
                    format=kwargs.get('format', None)
                )
                print ret[key]
            except NoReverseMatch:
                # Don't bail out if eg. no list routes exist, only detail routes.
                continue

        return Response(ret)
