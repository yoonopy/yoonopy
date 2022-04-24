from django.urls import path
# from .views import Join
from . import views

urlpatterns = [

	path('join/', views.Join.as_view(), name='join'),
	path('login/', views.Login.as_view(), name='login'),

]
