import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models
import datetime
# Create your views here.

@api_view(['GET'])
def checkRoomAvailability(request, roomId, date):
    month, day, year = [int(x) for x in date.split('-')]
    date_dt = datetime.date(year, month, day)
    reservations = list(models.Reservations.objects.filter(roomId=roomId, date=date_dt))
    room = models.Room.objects.get(roomId=roomId)
    reservedTimes = [(res.startTime, res.endTime) for res in reservations]
    reservedTimes.sort()
    freeTimes = []
    freeStart = room.openTime
    for start, end in reservedTimes:
        freeTimes.append((freeStart, start))
        freeStart = end
    
    if freeStart != room.closeTime:
        freeTimes.append((freeStart, room.closeTime))
            
    resp = {'availableTimes': [{"startTime": p[0], "endTime": p[1]} for p in freeTimes]}
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
            roomId=content["roomId"],
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


# @api_view(['POST'])
# def create_reservation(request):
#     """
#     Requires roomId, libraryName, type, minCapacity, maxCapacity
#     noiseLevel, openHour, closeHour, openMinute, closeMinute
#     in request body 
#     """
#     body_unicode = request.body.decode('utf-8')
#     body = json.loads(body_unicode)
#     content = body['content']
#     print(f'{content=}')
#     try:
#         student = models.Student.objects.get(pk=content['studentId'])
#         month, day, year = [int(x) for x in content['date'].split('-')]
#         date_dt = datetime.date(year, month, day)
#         startTime = datetime.time(content["startHour"], content["startMinute"])
#         endTime = datetime.time(content["endHour"], content["endMinute"])
#         models.Reservations.objects.create(
#             reservationID=content["reservationId"],
#             libraryName=content["libraryName"],
#             roomId=content["roomId"],
#             date=date_dt,
#             startTime=startTime,
#             endTime=endTime,
#             studentId=student
#         )
#     except models.Student.DoesNotExist as ex:
#         raise ex

#     return Response()


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