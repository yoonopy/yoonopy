from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed
from user.models import User
from rest_framework.response import Response
from .settings import MEDIA_ROOT
import os
from uuid import uuid4



class MainFeed(APIView):

	def get (self, request):
		print ("전체 피드 호출")
		feed_list = Feed.objects.all().order_by("-id")

		email = request.session.get('email', None)
		print(email)

		if not email: # 유저정보없이 접속시
			return render(request, 'user/login.html')

		user = User.objects.filter(email=email).first() # 회원정보
		if not user:
			return render(request, 'user/login.html')

		return render(request, "stagram/main.html", context=dict(feed_list=feed_list, user=user))

	def post(self, request):
		print("포스트 호출")
		return render(request, "stagram/main.html")


class Profile(APIView):
    	
	def get(self, request):
    		
		# 유저확인
		# 유저피드리스트
		email = request.session.get('email', None)
		print ("email ", email)
		if email is None:
			return render(request, 'user/login.html')

		user = User.objects.filter(email=email).first()
		print ("email", user)
		if user is None:
			return render(request, 'user/login.html')

		feed_list =	Feed.objects.filter(email=email).order_by("-id")
		print ("feed_list", feed_list)

		return render(request, 'stagram/profile.html',
						context=dict(
						feed_list=feed_list,
						user=user
						)
				)