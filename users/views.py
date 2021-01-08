from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, ProfileSerializer

User = get_user_model()


class UserProfileDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_url_kwarg = ("username",)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)


class ListFreelancers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


def become_freelancer(request):
    user = request.user
    if user.is_freelancer:
        return Response(data={'message': 'You already is a freelancer'}, status=status.HTTP_304_NOT_MODIFIED)
    user.is_freelancer = True
    user.save()
    return Response(status=status.HTTP_200_OK)


def un_become_freelancer(request):
    user = request.user
    if not user.is_freelancer:
        return Response(data={'message': 'You are not a freelancer'}, status=status.HTTP_400_BAD_REQUEST)
    # TODO: check if user has pending jobs, if has then return an appropriate response for that
    user.is_freelancer = False
    user.save()
    return Response(status=status.HTTP_200_OK)
