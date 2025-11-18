from django.urls import path
from .views import RegisterView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenSerializer

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
     path("login/", 
         TokenObtainPairView.as_view(serializer_class=CustomTokenSerializer),
         name="token_obtain_pair"),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
