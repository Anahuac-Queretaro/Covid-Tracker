from django.urls import path
from .views import InternalRegisterView


app_name = 'tracking'
urlpatterns = [
    path('', InternalRegisterView.as_view(), name='internal-register')
]
