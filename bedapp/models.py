from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class user(models.Model):
    uname = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.IntegerField(default=0)
    status = models.CharField(max_length=10)
    password = models.CharField(max_length=40)
    uphoto = models.ImageField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    condition = models.CharField(max_length=10)
    def __str__(self):
        return self.uname


class warden(models.Model):
    wname = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.IntegerField(default=0)
    password = models.CharField(max_length=40)
    wphoto = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.wname


class hostel(models.Model):
    email = models.EmailField()
    hstlname = models.CharField(max_length=255)
    hstltype = models.CharField(max_length=10)
    loc = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    img1 = models.ImageField(blank=True, null=True)
    img2 = models.ImageField(blank=True, null=True)
    img3 = models.ImageField(blank=True, null=True)
    img4 = models.ImageField(blank=True, null=True)
    img5 = models.ImageField(blank=True, null=True)
    hostel_license = models.FileField(blank=True, null=True)
    building_permit = models.FileField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    wifi = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    room_data = models.JSONField(blank=True, null=True)  # Field to store room data as JSON

    def __str__(self):
        return self.hstlname


class Room(models.Model):
    hostel = models.ForeignKey('hostel', on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50)


class Bed(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=50)
    bed_price = models.CharField(max_length=50)
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('booked', 'Booked'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    def __str__(self):
        return self.bed_number


class Booking(models.Model):
    user_name = models.CharField(max_length=40)
    user_email = models.EmailField()
    user_phone = models.IntegerField()
    hostel_name = models.CharField(max_length=255)
    room_id = models.CharField(max_length=10)
    bed_id = models.CharField(max_length=10)
    bed_price_per_day = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    checkin_date = models.DateField()
    checkout_date = models.DateField()

    def __str__(self):
        return f"{self.user_name} - {self.hostel_name} - {self.checkin_date} to {self.checkout_date}"


class Contact(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class PasswordReset(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    token = models.CharField(max_length=4)


class Booking_Archive(models.Model):
    user_name = models.CharField(max_length=40)
    user_email = models.EmailField()
    user_phone = models.IntegerField()
    hostel_name = models.CharField(max_length=255)
    room_id = models.CharField(max_length=10)
    bed_id = models.CharField(max_length=10)
    bed_price_per_day = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    checkin_date = models.DateField()
    checkout_date = models.DateField()

    def __str__(self):
        return f"{self.user_name} - {self.hostel_name} - {self.checkin_date} to {self.checkout_date}"
