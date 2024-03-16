
# Create your models here.
from django.db import models

class Reservations(models.Model):
    reservationID = models.AutoField(primary_key=True)
    libraryName = models.CharField(max_length=100)
    roomId = models.CharField(max_length=10)
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    studentId = models.ForeignKey('Student', on_delete=models.CASCADE)

class Student(models.Model):
    studentId = models.CharField(primary_key=True, max_length=10)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)

class Library(models.Model):
    libraryName = models.CharField(primary_key=True, max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

class Room(models.Model):
    roomId = models.CharField(primary_key=True, max_length=10)
    libraryName = models.ForeignKey('Library', on_delete=models.CASCADE)
    room_type = models.CharField(max_length=100)
    minCapacity = models.IntegerField()
    maxCapacity = models.IntegerField()
    noiseLevel = models.IntegerField()
    openTime = models.TimeField()
    closeTime = models.TimeField()

class Amenities(models.Model):
    roomId = models.ForeignKey('Room', on_delete=models.CASCADE)
    amenityName = models.CharField(max_length=100)
    # Make roomId and amenityName a composite primary key
    class Meta:
        unique_together = (('roomId', 'amenityName'))
