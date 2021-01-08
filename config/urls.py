"""dylance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_auth.registration.views import SocialAccountListView, SocialAccountDisconnectView, RegisterView

from users.views import TwitterLogin, TwitterConnect, FacebookConnect, FacebookLogin, ConfirmEmailView

admin.autodiscover()

app_name = "dylance"

EMAIL_CONFIRMATION = r'^auth/confirm-email/(?P<key>[-:\w]+)$'
# NOTE: If you change this URL you have to update the callback URL
# in the OAuth providers' accounts, too
OAUTH_CALLBACK = 'auth/social/{provider}/callback'

# URL patterns

fb_urlpatterns = [
    path('login/', FacebookLogin.as_view(), name='fb_login'),
    path('connect/', FacebookConnect.as_view(), name='fb_connect'),
]

twitter_urlpatterns = [
    path('login/', TwitterLogin.as_view(), name='twitter_login'),
    path('connect/', TwitterConnect.as_view(), name='fb_connect'),
]

auth_urlpatterns = [
    path('', include('rest_auth.urls')),
    path('social/facebook/', include(fb_urlpatterns)),
    path('social/twitter/', include(twitter_urlpatterns)),
    path(
        'user/accounts/',
        SocialAccountListView.as_view(),
        name='social_account_list',
    ),
    path(
        'user/accounts/<int:pk>/disconnect/',
        SocialAccountDisconnectView.as_view(),
        name='social_account_disconnect',
    ),
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('register/account-confirm-email/<key>',
         ConfirmEmailView.as_view(), name='account_confirm_email'),
]

api_urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(auth_urlpatterns)),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('jobs/', include(('jobs.urls', 'search'), namespace='jobs')),
]

urlpatterns = [
    # The SPA serves these URLs but the backend has to know
    # where they point to for reference, don't change the url names.
    path(
        OAUTH_CALLBACK.format(provider='facebook'),
        TemplateView.as_view(),
        name='facebook_callback',
    ),
    # This has to be last because rest_auth.registration.urls
    # also defines `account_confirm_email` what we override above.
    path('', include(api_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
