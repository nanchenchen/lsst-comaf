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

    owner = UserSerializer(required=False)

    class Meta:
        model = metrics_models.Metric
        fields = ('id', 'name', 'owner', 'opsim_run', 'maf_comment', 'created_at', )

class MetricUploadSerializer(serializers.Serializer):
    key = serializers.CharField()
    data = MetricSerializer()

class MetricsSerializer(serializers.Serializer):
    metrics = serializers.ListField(child=MetricSerializer(), required=False)

class PlotSerializer(serializers.ModelSerializer):
    metric = MetricSerializer

    class Meta:
        model = metrics_models.Plot
        fields = ('metric', 'type', 'src')