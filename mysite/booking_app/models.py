from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class Country(models.Model):
    country_name = models.CharField(max_length=50, unique=True)
    country_image = models.ImageField(upload_to='country_image')

    def __str__(self):
        return self.country_name


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),
                                                       MaxValueValidator(60)],
                                           null=True, blank=True)
    photo = models.ImageField(upload_to='image_user', null=True, blank=True)
    ROLE_CHOICES = (
    ('client', 'client'),
    ('owner', 'owner'))
    user_role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='client')
    phone = PhoneNumberField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'




class City(models.Model):
    city_name = models.CharField(max_length=50)
    city_image = models.ImageField(upload_to='city_image')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.country}, {self.city_name}'


class Service(models.Model):
    service_image = models.ImageField(upload_to='service_image')
    service_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.service_name


class Hotel(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_hotel')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    postal_code = models.PositiveIntegerField(unique=True, verbose_name="Почта номери")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_hotel')
    hotel_stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                               MaxValueValidator(5)],
                                                   null=True, blank=True)
    hotel_video = models.FileField(upload_to='hotel_videos', null=True, blank=True)
    description = models.TextField()
    service = models.ManyToManyField(Service)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return self.hotel_name

    def get_avg_rating(self):
        rating = self.review.all()
        if rating.exists():
            return round(sum([i.stars for i in rating]) / rating.count(), 1 )
        return 0

    def get_count_people(self):
        return self.review.count()


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_image')
    image = models.ImageField(upload_to='hotel_image')

    def __str__(self):
        return f'{self.hotel}, {self.image}'


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_room')
    room_number = models.PositiveIntegerField()
    ROOM_TYPE_CHOICES = (
    ('стандарт', 'стандарт'),
    ('семейный', 'семейный'),
    ('одноместный', 'одноместный'),
    ('люкс', 'люкс'))
    room_type = models.CharField(max_length=15, choices=ROOM_TYPE_CHOICES)
    ROOM_STATUS_CHOICES = (
    ('занят', 'занят'),
    ('забронирован', 'забронирован'),
    ('свободен', 'свободен'))
    room_status = models.CharField(max_length=15, choices=ROOM_STATUS_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f'{self.hotel}, {self.room_number}'


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_image')

    def __str__(self):
        return f'{self.room}, {self.image}'


class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_booking')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.hotel}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='review')
    stars = models.PositiveIntegerField(choices=[(i, str(i))for i in range(1, 6)])
    text = models.TextField()
    created_date = models.DateTimeField()

    def __str__(self):
        return f'{self.user}, {self.hotel}'
