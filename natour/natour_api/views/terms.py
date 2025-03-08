from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Term
from ..serializer import TermSerializer

# Rota para listagem de Termos de Uso e Política de Privacidade
@api_view(['GET'])
def get_term(request):
    term = Term.objects.all()
    return Response(TermSerializer(term, many=True).data)

# Rota para cadastro de Termos de Uso e Política de Privacidade
@api_view(['POST'])
def add_terms(request):
    serializer = TermSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Edição dos Termos de Uso e Política de Privacidade
@api_view(['PUT'])
def update_terms(request, pk):
    terms = get_object_or_404(Term, pk=pk)
    serializer = TermSerializer(terms, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    