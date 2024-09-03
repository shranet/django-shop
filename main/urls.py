from django.urls import path

from main.views import MainIndex

app_name = 'main'
urlpatterns = [
    path('', MainIndex.as_view(), name='index')
]
