import logging
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from ..models import CustomUser
from ..serializer import CustomUserSerializer
from ..pagination import CustomPagination

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_count(request):
    user_count = CustomUser.objects.count()
    return Response({"total_users": user_count})

# qnt de ativos/intaivos
# por mês
# qnt de pontos
# ranking de pontso por reviews