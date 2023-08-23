from django.urls import include, path
from rest_framework.routers import DefaultRouter

from binance_automation.users.views.user import (
    UserDocumentTypeViewSet, 
    UserTypeViewSet,
    # RegisterViewSet, 
    # LoginViewSet,
    
    UserViewSet
)
app_name = "Users"

router = DefaultRouter()

router.register(r'type', UserTypeViewSet, basename='user_type')
router.register(r'doc_type', UserDocumentTypeViewSet, basename='user_document_type')
# router.register(r'register', RegisterViewSet, basename='register_user')
# router.register(r'login', LoginViewSet, basename='login_user')

router.register(r'', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
]

