import json
from django.shortcuts import render
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models
from .utils.fcns import *
import datetime
import random
# Create your views here.

UNAVAILABLE = None
MAX_RESERVATION_ID = 100000000
TOTAL_BUFFER_DAYS = 5


@api_view(['GET'])
def checkRoomAvailability(request, roomId):
    reservations = list(models.Reservations.objects
                        .filter(roomId=roomId, studentId=UNAVAILABLE)
                        .values('date', 'startTime', 'endTime'))
            
    resp = {'availableTimes': reservations}
    return Response(resp)

@api_view(['POST'])
def create_room(request):
    """
    Requires roomId, libraryName, type, minCapacity, maxCapacity
    noiseLevel, openHour, closeHour, openMinute, closeMinute
    in request body 
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['content']
    print(f'{content=}')
    try:
        library = models.Library.objects.get(pk=content['libraryName'])
        openTime = datetime.time(content["openHour"], content["openMinute"])
        closeTime = datetime.time(content["closeHour"], content["closeMinute"])
        models.Room.objects.create(
            roomId=content['roomId'],
            libraryName=library,
            type=content["type"],
            minCapacity=content["minCapacity"],
            maxCapacity=content["maxCapacity"],
            noiseLevel=content["noiseLevel"],
            openTime=openTime,
            closeTime=closeTime,
        )
    except models.Library.DoesNotExist as ex:
        raise ex

    return Response()


@api_view(['POST'])
def create_reservation(request):
    """
    Requires roomId, libraryName, type, minCapacity, maxCapacity
    noiseLevel, startHour, endHour, startMinute, endMinute
    in request body 
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['content']
    print(f'{content=}')


    try:
        student = models.Student.objects.get(pk=content['studentId'])
        print(f'{student}')
        room = models.Room.objects.get(roomId=content['roomId'])
        print(f'{room=}')
    except models.Student.DoesNotExist as ex:
        raise ex
    except models.Room.DoesNotExist as ex:
        raise ex
    
    
    year, month, day = [int(x) for x in content['date'].split('-')]
    date_dt = datetime.date(year, month, day)
    startTime = datetime.time(content["startHour"], content["startMinute"])
    endTime = datetime.time(content["endHour"], content["endMinute"])
    if date_dt < datetime.date.today() or \
        date_dt == datetime.date.today and startTime < datetime.datetime.now().time():
        raise ValueError("Requested date is already past")
    
    
    
    reservations = list(models.Reservations.objects.filter(
        studentId=None,
        roomId=content['roomId'],
        date=date_dt,
        startTime__lte=startTime,
        endTime__gte=endTime))
    
    if len(reservations) != 1:
        raise ValueError("Section is already reserved/is not open at this time")

    leftStart = reservations[0].startTime
    rightEnd = reservations[0].endTime
    reservations[0].startTime = startTime
    reservations[0].endTime = endTime
    reservations[0].studentId = student
    print(reservations[0])
    reservations[0].save()

    if leftStart < startTime:
        models.Reservations.objects.create(
            libraryName=content["libraryName"],
            roomId=content["roomId"],
            date=date_dt,
            startTime=leftStart,
            endTime=startTime,
            studentId=None
        )
    
    if rightEnd > endTime:
        models.Reservations.objects.create(
            libraryName=content["libraryName"],
            roomId=content["roomId"],
            date=date_dt,
            startTime=endTime,
            endTime=rightEnd,
            studentId=None
        )

    return Response()


@api_view(['POST'])
def create_library(request):
    """
    Requires libraryName, location, phone in request body
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['content']
    print(f'{content=}')
    models.Library.objects.create(
        libraryName=content["libraryName"],
        location=content["location"],
        phone=content["phone"]
    )

    return Response()

@api_view(['GET'])
def get_all_rooms(request):
    rooms = models.Room.objects.all().values()
    return Response(rooms)

@api_view(['GET'])
def get_all_reservations(request):
    res = models.Reservations.objects.all().values()
    return Response(res)

@api_view(['GET'])
def get_all_active_reservations(request):
    res = models.Reservations.objects.filter(studentId=None).values()
    return Response(res)

@api_view(['POST'])
def create_student(request):
    """
    Requires studentId, email, phone in request body
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['content']
    print(f'{content=}')
    models.Student.objects.create(
        studentId=content["studentId"],
        email=content["email"],
        phone=content["phone"]
    )

    return Response()

# Raises a error, but still makes the objects.  Figure out later
@api_view(['POST'])
def adminUpdateBuffer(request):
    today = datetime.date.today()
    pastReservations = models.Reservations.objects.filter(date__lt=today).order_by('date')
    earliest = pastReservations.first()
    noEntries = False
    if earliest is None:
        daysElapsed = datetime.timedelta(days=TOTAL_BUFFER_DAYS)
        noEntries = True
    else:
        daysElapsed = today - earliest.date
    
    # Want to store/update this date every buffer update
    # so don't have to query whole reservation set every time but not important rn
    lastReservation = models.Reservations.objects.filter(date__gte=today).order_by('-date').first()
    if lastReservation is None:
        if noEntries:
            latest = today
        else:
            return Response()
    else:
        latest = lastReservation.date + daysElapsed

    rooms = models.Room.objects.all()
    newReservations = []
    for room in rooms:
        for i in range(int(daysElapsed/datetime.timedelta(days=1))):
            newReservations.append(models.Reservations.objects.create(               
                libraryName=room.libraryName,
                roomId=room.roomId,
                date=latest + datetime.timedelta(days=i),
                startTime=room.openTime,
                endTime=room.closeTime,
                studentId=None
            ))
    print(newReservations)
    try:
        models.Reservations.objects.bulk_create(newReservations)
    except IntegrityError:
        pass
    
    return Response()
    
@api_view(['DELETE'])
def clearAllTimeSlots(request):
    models.Reservations.objects.all().delete()
    return Response()
