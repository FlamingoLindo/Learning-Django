from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Point
from ..serializer import PointSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_point(request):
    serializer = PointSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_points(request):
    points = Point.objects.all()
    return Response(PointSerializer(points, many=True).data)

@api_view(['PUT'])
def change_point_status(request, pk):
    point = get_object_or_404(Point, pk=pk)

    serializer = PointSerializer(point, data=request.data)
    point_creator = point.user
    creator_email = point_creator.email

    if point.active == False:
        send_mail(
            'Ponto desativado!',
            f'Olá! {creator_email}\nInfelizmente, seu ponto foi desativado.',
            'natourproject@gmail.com',
            [creator_email]
        )
    else:
        pass
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def point_detail(request, pk):
    point = get_object_or_404(Point, pk=pk)

    if request.method == 'GET':
        point.views += 1
        point.save()
        return Response(PointSerializer(point).data)
    
    elif request.method == 'PUT':
        serializer = PointSerializer(point, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'DELETE':
        point.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
