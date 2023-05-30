from rest_framework.views import APIView

from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import generics, permissions
# from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# Register API
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User
from accounts.models import *
from accounts.serializers import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings


@api_view(["POST"])
def signup(request):
    if "username" not in request.data or "password" not in request.data or "password2" not in request.data:
        return Response({"message": "fill all fields"})
    name = request.data["username"]
    password = request.data["password"]
    password2 = request.data["password2"]

    if password != password2:
        return Response({"message": "passwords not match"})

    user = User.objects.create(
        username=name,
    )
    user.set_password(password)
    user.save()
    return Response({"message": "user created"})


class Logoutview(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # try:
        refresh_token = request.data["refresh_token"]
        # token = RefreshToken(refresh_token)
        # token.blacklist()
        # OutstandingToken.objects.filter(user=request.user).delete()

        OutstandingToken.objects.filter(user=request.user).delete()

        return Response({"message": 'user logout'})
    # except Exception as e:
    #     return Response({"message": 'failed to logout,user not Atenticatid'})


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response(status=status.HTTP_205_RESET_CONTENT)


# @api_view(["POST","GET"])
# def user_profile(request):
#     profile = Profile.objects.get(user_id=request.user.id)
#
#     return Response(profile)

# @api_view(["GET",])
# @permission_classes([IsAuthenticated,])
# def get_me(request):
#     model = User
#     permission_classes = [IsAuthenticated]
#     token_header = request.META.get('HTTP_AUTHORIZATION')
#     # if token_header is not None and 'Token' in token_header:
#     # user=User
#     # token = token_header.split(' ')[1]
#     user = OutstandingToken.objects.filter(user_id=request.user)
#     # user=tokens.objects.get(key=token).user
#     return Response({
#         "user_id":user.id,
#         "username":user.username,
#         "phone":user.phone,
#         "is_staff":user.is_staff,
#         "email":user.email,
#         "is_superuser":user.is_superuser,
#         # 'slides':user
#
#
#     })


# @api_view(['DELETE'])
# def logout(request):
#     try:
#         authentication = JWTAuthentication()
#         user, token = authentication.authenticate(request)
#         tokens = OutstandingToken.objects.filter(user=user)
#         for outsending_token in tokens:
#             BlacklistedToken.objects.create(token=outsending_token)
#             token.delete()
#         return Response({'message': 'success logout'}, status=status.HTTP_200_OK)
#     except AuthenticationFailed:
#         return Response({'message': 'Failed to logout ,User not Authenticate'})


# @api_view(['POST'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     # برای لاگ‌اوت، توکن جاری را از سیستم حذف می‌کنیم
#     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#     payload = jwt_payload_handler(request.user)
#     token = jwt_encode_handler(payload)
#     request.user.auth_token.delete()
#     return Response({'success': 'Successfully logged out.'})


# class LogoutView(APIView):
#     authentication_classes = [JSONWebTokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         # برای لاگ‌اوت، توکن جاری را از سیستم حذف می‌کنیم
#         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#         payload = jwt_payload_handler(request.user)
#         token = jwt_encode_handler(payload)
#         request.user.auth_token.delete()
#         return Response({'success': 'Successfully logged out.'})

# @api_view(["POST","GET"])
# def user_profile(request):
#     profile = Profile.objects.get(user_id=request.user.id)
#     return Response(profile)

# @api_view(['POST'])
# def register_with_token(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#
#     if not username or not password:
#         return Response({'error': 'Please provide both username and password'},
#                         status=status.HTTP_400_BAD_REQUEST)
#
#     user = User.objects.create_user(username=username, password=password)
#     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#     payload = jwt_payload_handler(user)
#     token = jwt_encode_handler(payload)
#
#     return Response({'token': token}, status=status.HTTP_201_CREATED)
#
#
# class UserProfileView(APIView):
#     authentication_classes = [JSONWebTokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         user = request.user
#         return Response({'username': user.username, 'email': user.email})


# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#
#     def post(self, request, *args, **kwargs):
#         expires = timezone.now() + timezone.timedelta(days=30)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#         "user": UserSerializer(user, context=self.get_serializer_context()).data,
#
#         "token": Token.objects.get_or_create(user,expiry=expires)[1]
#         })

# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         # login(request, user)
#         # return super(LoginAPI, self).post(request, format=None)
#         aa,bb=JWTAuthentication.authenticate(request)
#         return Response({aa:"ss"})

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'message': 'Password updated successfully',
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#


class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProfileUpdate(APIView):
#     def put(self,request):
#         # user = request.user
#         serializer = ProfileUpdateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors)


# @api_view(['PUT'])
# def profile_update(request):
#     # user = request.user
#     serializer = ProfileUpdateSerializer( data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProfileView(APIView):
#     def get(self, request):
#         profile = Profile.objects.first() # یا هر دیگر روشی برای گرفتن پروفایل
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data)
#
#     def put(self, request):
#         profile = Profile.objects.first() # یا هر دیگر روشی برای گرفتن پروفایل
#         serializer = ProfileSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDispatcher(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        return ProfileView.as_view()(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return CreateProfileView.as_view()(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return UpdateProfileView.as_view()(request,*args,**kwargs)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request._request.user.profile


class CreateProfileView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


from django.shortcuts import render

# Create your views here.
