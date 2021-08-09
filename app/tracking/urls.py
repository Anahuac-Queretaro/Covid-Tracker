from django.urls import path
from .views import (
    InternalRegisterView,
    ExternalRegisterView,
    AlertView
)


app_name = 'tracking'
urlpatterns = [
    path('', InternalRegisterView.as_view(), name='internal-register'),
    path('external/', ExternalRegisterView.as_view(), name='external-register'),
    path('alert/', AlertView.as_view(), name='alert')
]
