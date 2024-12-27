from rest_framework import serializers


class StringListField(serializers.ListField):
    child = serializers.CharField()


class SampleSerializer(serializers.Serializer):
    names = StringListField()
