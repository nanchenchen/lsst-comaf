"""
The view classes below define the API endpoints.

"""

from rest_framework import status
from rest_framework.views import APIView, Response
from django.core.urlresolvers import NoReverseMatch
from rest_framework.reverse import reverse
from rest_framework.compat import get_resolver_match, OrderedDict
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets

import comaf.apps.metrics.models as metrics_models
from comaf.apps.api import serializers
import os
from django.contrib.auth import get_user_model
User = get_user_model()

import logging

logger = logging.getLogger(__name__)

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

class MetricsView(viewsets.ModelViewSet):
    #queryset = metrics_models.Metric.objects.all()
    serializer_class = serializers.MetricSerializer
    paginate_by = 10

    def get_queryset(self):
        queryset = metrics_models.Metric.objects.all()
        params = self.request.query_params
        if params.get("user"):
            owner_id = params.get("user")
            queryset = queryset.filter(owner__id=owner_id)

        return queryset

    def post(self, request, format=None):
        input = serializers.MetricUploadSerializer(data=request.data)
        if input.is_valid():
            parsed_data = input.validated_data
            metrics_models.create_from_post(parsed_data["key"], parsed_data["data"])
            return Response(parsed_data["data"], status=status.HTTP_200_OK)
        return Response(input.errors, status=status.HTTP_400_BAD_REQUEST)

class PlotView(APIView):

    parser_classes = (FileUploadParser, )

    def post(self, request, format='png'):
        import pdb
        pdb.set_trace()
        up_file = request.data['image']
        destination = open('/tmp/plots/' + up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
            destination.close()

        # ...
        # do some stuff with uploaded file
        # ...
        return Response(up_file.name, status.HTTP_201_CREATED)


class CommentView(APIView):

    def get(self, request, metric_id, format=None):
        comments = metrics_models.Comment.objects.filter(metric__id=metric_id).all()
        #data = {
            #"metric": metrics_models.Metric.objects.get(id=metric_id),
        #    "comments": comments}
        output = serializers.CommentSerializer(comments, many=True)

        return Response(output.data, status=status.HTTP_200_OK)
        #return Response(output.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, metric_id, format=None):
        input = serializers.CommentSerializer(data=request.data)
        if input.is_valid():
            text = input.validated_data['text']
            metric = metrics_models.Metric.objects.get(id=metric_id)
            user = User.objects.get(id=self.request.user.id)
            comment = metrics_models.Comment(metric=metric, owner=user, text=text)
            comment.save()
            output = serializers.CommentSerializer(comment)
            return Response(output.data, status=status.HTTP_200_OK)

        return Response(input.errors, status=status.HTTP_400_BAD_REQUEST)