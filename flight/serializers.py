from django.db.models.fields import IntegerField
from rest_framework import serializers
from .models import Flight, Passenger, Reservation
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token


class FlightSerializer(serializers.ModelSerializer):
 class Meta:
  model = Flight
  fields = ['flightNumber', 'operatingAirlines', 'departureCity','dateOfDeparture']
  
class PassengerSerializer(serializers.ModelSerializer):
  flight = serializers.StringRelatedField() # ismin görülmesi icin
  flight_id = serializers.IntegerField()  # StringRelatedField kullanirsak Post a izin vermiyor. Bunu ezmek icin flight_id yi Integerfield yapip readOnly den kurtariyoruz. Post yaparken flight_id yi göndermemiz yeterli oluyor
  user = serializers.StringRelatedField()
  user_id = serializers.IntegerField()
  class Meta:
    model = Passenger
    fields = ['flight','flight_id','user','user_id','firstName', 'lastName', 'email', 'phone']
  

class ReservationSerializer(serializers.ModelSerializer):
  flight = serializers.StringRelatedField()
  flight_id = serializers.IntegerField()
  passenger = serializers.StringRelatedField()
  passenger_id = serializers.IntegerField()
  user = serializers.StringRelatedField()
  user_id = serializers.IntegerField()
  # passengers = serializers.SerializerMethodField()
  class Meta:
    model = Reservation
    fields = ['flight','flight_id', 'passenger','passenger_id','user','user_id']
  # def get_passengers(self,obj):
  #     passengers_data = Passenger.objects.all()
  #     serializer = PassengerSerializer(passengers_data, many=True)
  #     return serializer.data

  
class UserSerializer(serializers.ModelSerializer):
 class Meta:
  model = User
  fields = ['id', 'username', 'password']
  
  # password görünmesin diye
  extra_kwargs = {
   'password':{
       'write_only':True,
       'required' : True
   }
  }

 def create(self,validated_data):
  user = User.objects.create_user(**validated_data)
  Token.objects.create(user=user)
  return user
  
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
# user ile islem yapmak icin bu serializers olusturuldu