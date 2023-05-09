
# Create your models here.
from django.db import models

# Create reservations model with fields libraryName, roomId, date, startTime, endTime, and studentId
class Reservations(models.Model):
    reservationID = models.AutoField(primary_key=True)
    libraryName = models.CharField(max_length=100)
    roomId = models.IntegerField()
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    studentId = models.ForeignKey('Student', on_delete=models.CASCADE)

# Create student model with email and phone number
class Student(models.Model):
    studentId = models.CharField(primary_key=True, max_length=10)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)

# Create library model with libraryName, location and phone number
class Library(models.Model):
    libraryName = models.CharField(primary_key=True, max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

# Create room model with libraryName, type, minCapacity, maxCapacity, and noiseLevel
class Room(models.Model):
    roomId = models.CharField(primary_key=True, max_length=10)
    libraryName = models.ForeignKey('Library', on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    minCapacity = models.IntegerField()
    maxCapacity = models.IntegerField()
    noiseLevel = models.IntegerField()

# Create amenities model with room id and amenity name (both primary keys, with roomId being a foreign key)
class Amenities(models.Model):
    roomId = models.ForeignKey('Room', on_delete=models.CASCADE)
    amenityName = models.CharField(max_length=100)
    # Make roomId and amenityName a composite primary key
    class Meta:
        unique_together = (('roomId', 'amenityName'))