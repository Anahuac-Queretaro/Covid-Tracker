from django.urls import path
from .views import InternalRegisterView, ExternalRegisterView


app_name = 'tracking'
urlpatterns = [
    path('', InternalRegisterView.as_view(), name='internal-register'),
    path('external/', ExternalRegisterView.as_view(), name='external-register')
]
