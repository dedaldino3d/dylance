from allauth.account.models import EmailConfirmationHMAC, EmailConfirmation
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from rest_auth.registration.views import SocialLoginView, SocialConnectView
from rest_auth.social_serializers import TwitterLoginSerializer, TwitterConnectSerializer
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, ProfileSerializer

User = get_user_model()


class FacebookMixin:
    adapter_class = FacebookOAuth2Adapter


class FacebookLogin(FacebookMixin, SocialLoginView):
    """
       Logs the user in with the providers data.
       Creates a new user account if it doesn't exist yet.
    """


class FacebookConnect(FacebookMixin, SocialConnectView):
    """
        Connects a provider's user account to the currently logged in user.
    """


class TwitterMixin:
    adapter_class = TwitterOAuthAdapter


class TwitterLogin(TwitterMixin, SocialLoginView):
    serializer_class = TwitterLoginSerializer


class TwitterConnect(TwitterMixin, SocialConnectView):
    """
        Connects a provider's user account to the currently logged in user.
    """
    serializer_class = TwitterConnectSerializer


class ConfirmEmailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return HttpResponseRedirect('/login/success')

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return HttpResponseRedirect('/login/failure')
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs


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
