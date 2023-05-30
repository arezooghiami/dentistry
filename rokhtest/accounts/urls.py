# from .views import RegisterAPI
from rest_framework_simplejwt import views as jwt_views
from django.urls import path , include
from knox import views as knox_views
from . import views
# from .views import JWTAuthentication,LoginAPI
from .views import *
from django.urls import path
# from .views import LogoutView
# from .views import UserProfileView
from django.urls import path, include
from rest_framework import routers
from .views import *

#
# router = routers.SimpleRouter()
# router.register(r'profiles',ProfileViewset,basename=Profile)
# router.register(r'profiles', ProfileViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',signup),
    path('users/', UserCreate.as_view(), name='user_create'),
    path('logout/', Logoutview.as_view(), name='logout'),
    path('logout_all/' ,LogoutAllView.as_view(), name='logoutall'),
    path('change/', ChangePasswordView.as_view(), name='change-password'),
    # path('update/',ProfileUpdate.as_view(),name='profile_update'),
    # path('profile/', profile_update, name='profile_update'),
    # path('profile/',views.ProfileDispatcher.as_view(),name="profile_dispathcher"),
    path('profile/', ProfileView.as_view()),
    path('profile/create/', CreateProfileView.as_view(), name='create_profile'),
    # path('profile/update/', UpdateProfileView.as_view(), name='update_profile')
]