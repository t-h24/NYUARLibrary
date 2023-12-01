# django-react-docker/backend/backend/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import Reservations


@api_view(['GET'])
def send_some_data(request):
    return Response({
        "data": "Hello from django backend"
    })


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ['reservationID', 'libraryName', 'roomId', 'date', 'startTime', 'endTime', 'studentId']


#get all reservation of a student with studentId
#sample url: http://localhost:8000/reservations/?studentId=123456
@api_view(['GET'])
def get_all_reservations(request):
    studentId = request.GET.get('studentId')
    reservations = Reservations.objects.filter(studentId=studentId)
    if reservations is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)
    
    