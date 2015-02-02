from django.contrib.auth.models import User
from gebouw.models import Complex
from rest_framework import serializers


class GebruikerSerializer(serializers.ModelSerializer):
    complexadmin = serializers.PrimaryKeyRelatedField(many=True, queryset=Complex.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'complexadmin')