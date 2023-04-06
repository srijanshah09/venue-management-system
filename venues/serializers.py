from rest_framework import serializers

from .models import (
    State,
    City,
)

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id','name', 'is_active']


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id', 'name', 'state', 'is_active']
        # depth = 1

    def create(self, validated_data):
        print(validated_data)
        state = State.objects.get(pk=validated_data.get('state'))
        is_active = True if validated_data['is_active'] else False
        return City.objects.create(name = validated_data['name'], is_active = is_active, state=state)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.is_active = validated_data.get('is_active',instance.is_active)
        if validated_data.get('state') :
            instance.state = State.objects.get(pk=validated_data.get('state'))
        else :
            instance.state = instance.state
        instance.save()