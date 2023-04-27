from rest_framework import serializers

class ApiSerializer(serializers.Serializer):
    tree = serializers.CharField()

