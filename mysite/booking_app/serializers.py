from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



class UserProfileRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'first_name', 'last_name',
                  'age')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_image']



class CountrySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name', 'country_image']


class HotelCountrySerializer(serializers.ModelSerializer):
    country = CountrySimpleSerializer()
    class Meta:
        model = Hotel
        fields = ['country']


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'username']

    def get_queryset(self):
        return UserProfile.objects.all(id=self.request.user.id)



class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'user_role']

    def get_queryset(self):
        return UserProfile.objects.all(id=self.request.user.id)


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'photo']


class CityListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = ['id', 'city_name', 'country', 'city_image']



class CitySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_name', 'service_image']


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = '__all__'



class HotelListSerializer(serializers.ModelSerializer):
    hotel_image = HotelImageSerializer(many=True, read_only=True)
    city = CitySimpleSerializer()
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'city', 'hotel_image', 'hotel_stars', 'description', 'avg_rating', 'count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_type']


class ReviewDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    hotel = HotelCountrySerializer()

    class Meta:
        model = Review
        fields = ['user', 'hotel', 'text']


class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_image = HotelImageSerializer(many=True, read_only=True)
    city = CitySimpleSerializer()
    country = CountrySimpleSerializer()
    service = ServiceSerializer(many=True)
    owner = UserProfileDetailSerializer()
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    hotel_room = RoomListSerializer(many=True, read_only=True)
    review = ReviewDetailSerializer(many=True, read_only=True)


    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'street', 'postal_code', 'city', 'country', 'hotel_image',
                  'hotel_video', 'hotel_stars', 'description', 'service', 'owner', 'avg_rating',
                  'count_people', 'hotel_room', 'review']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

class HotelSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['hotel_name']


class CityDetailSerializer(serializers.ModelSerializer):
    hotel = HotelListSerializer()

    class Meta:
        model = City
        fields = ['city_name', 'hotel']

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = '__all__'



class RoomDetailSerializer(serializers.ModelSerializer):
    hotel = HotelSimpleSerializer()
    image = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['hotel', 'room_number', 'image', 'room_type', 'room_status', 'price', 'description']


class RoomSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_number']


class BookingSerializer(serializers.ModelSerializer):
    user = UserProfileDetailSerializer()
    hotel = HotelSimpleSerializer()
    room = RoomSimpleSerializer()
    class Meta:
        model = Booking
        fields = ['id', 'user', 'hotel', 'room', 'check_in', 'check_out']



class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileDetailSerializer()
    hotel = HotelSimpleSerializer()

    class Meta:
        model = Review
        fields = ['user', 'hotel', 'stars', 'text', 'created_date']
