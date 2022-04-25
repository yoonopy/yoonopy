from django.urls import path
from . import views

urlpatterns = [
		# html이름 , class이름, 
	path('join/', views.Join.as_view(), name='join'),
	path('login/', views.Login.as_view(), name='login'),
	path('logout/', views.Logout.as_view()),
	path('update_profile/', views.UpdateProfile.as_view(), name='update_profile'),

]
