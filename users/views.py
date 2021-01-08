from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializers import UserSerializer, ProfileSerializer

User = get_user_model()


class UserProfileDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_url_kwarg = ("username",)


class ListFreelancers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
