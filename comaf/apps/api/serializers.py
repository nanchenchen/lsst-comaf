"""
This module defines serializers for the main API data objects:

.. autosummary::
    :nosignatures:

    MetricSerializer

"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

import comaf.apps.metrics.models as metrics_models

User = get_user_model()

# A simple string field that looks up dimensions on deserialization
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff',)


class MetricSerializer(serializers.ModelSerializer):
    #owner = UserSerializer(required=False)
    #owner = UserSerializer()

    class Meta:
        model = metrics_models.Metric
        fields = ('id', 'name', 'owner', 'opsim_run', 'maf_comment', 'created_at', )


class MetricUploadSerializer(serializers.Serializer):
    key = serializers.CharField()
    data = MetricSerializer()


class MetricListSerializer(serializers.Serializer):
    metrics = serializers.ListField(child=MetricSerializer(), required=False)


class PlotSerializer(serializers.ModelSerializer):
    metric = MetricSerializer()

    class Meta:
        model = metrics_models.Plot
        fields = ('metric', 'type', 'src')


class CommentSerializer(serializers.ModelSerializer):
    #metric = MetricSerializer(required=False)
    #owner = UserSerializer(required=False)

    class Meta:
        model = metrics_models.Comment
        fields = ('id', 'metric', 'owner', 'created_at', 'text', )
        read_only_fields = ('created_at', 'metric', 'owner',)


class CommentListSerializer(serializers.Serializer):
    metric = MetricSerializer(required=False)
    comments = serializers.ListField(child=CommentSerializer(), required=False, read_only=True)