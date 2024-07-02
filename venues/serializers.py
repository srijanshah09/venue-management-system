from rest_framework import serializers

from .models import (
    State,
    City,
    Address,
    BankAccount,
    Venue,
    Availability,
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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','first_line', 'city', 'pincode']


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'account_holder_name', 'bank_name', 'ifsc_code', 'account_number', 'account_type', 'nick_name']

    def create(self, validated_data):
        return BankAccount(**validated_data)

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'day', 'is_open']

class VenueSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    bank_account = BankAccountSerializer()
    days = AvailabilitySerializer(many=True)

    class Meta:
        model = Venue
        fields = ['id','title','map_link', 'address', 'contact', 'bank_account', 'is_active', 'days']

    def create(self, validated_data):
        address_instance = validated_data.pop('address')
        account_instance = validated_data.pop('bank_account')
        days_data = validated_data.pop('days') or None
        address = Address.objects.create(**address_instance)
        account = BankAccount.objects.create(user=self.context['request'].user, **account_instance)
        instance = Venue.objects.create(owner=self.context['request'].user, address = address, bank_account=account, **validated_data)
        if days_data:
            for a in days_data:
                Availability.objects.create(venue = instance, **a)
        return instance        
    

    # def update(self, instance, validated_data):
    #     address_instance = validated_data.pop('address')
    #     account_instance = validated_data.pop('bank_account')
    #     days_data = validated_data.pop('days') or None
    #     address = Address.objects.get(pk=address_instance["id"])
    #     address.update(**address_instance)
    #     account = BankAccount.objects.get(id=account_instance["id"])
    #     account.update(**account_instance)
    #     instance = Venue.objects.get(  id = validated_data["id"])
    #     instance.update(address = address, bank_account=account, **validated_data)
    #     if days_data:
    #         for a in days_data:
    #             day = Availability.objects.get(id=a["id"])
    #             day.update(venue = instance, **a)
    #     return instance 