from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Review, Point, CustomUser
from ..serializer import ReviewSerializer

#verificar média ao deletar tbm

# Rota para criação de 'review' com comentário e avaliação em forma de estrelas
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_point(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        review = serializer.save()
        
        point = review.point
        point.score = Review.objects.filter(point=point).aggregate(Avg('star'))['star__avg']
        point.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retorna todos as avaliações
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_reviews(request):
    reviews = Review.objects.all()
    return Response(ReviewSerializer(reviews, many=True).data)

# Rertorna avaliação especifica
# Não é melhor fazer uma q retorna as avalizações do usuário?????
@api_view(['GET'])
def point_reviews(request, pk):
    reviews = Review.objects.filter(point=pk)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'GET':
        return Response(ReviewSerializer(review).data)
    
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
