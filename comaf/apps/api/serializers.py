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


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = metrics_models.OpSimRun
        fields = ('id', 'name',)


class MetricSerializer(serializers.ModelSerializer):

    opsim_run = RunSerializer(required=False)
    owner = UserSerializer(required=False)

    class Meta:
        model = metrics_models.Metric
        fields = ('id', 'name', 'owner', 'opsim_run', 'maf_comment', 'created_at', )

class MetricsSerializer(serializers.Serializer):
    metrics = serializers.ListField(child=MetricSerializer(), required=False)
