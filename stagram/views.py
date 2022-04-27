from django.shortcuts import render
from rest_framework.views import APIView
from content.models import Feed
from user.models import User
from content.models import Like, Bookmark, Comment
from .settings import MEDIA_ROOT
import os
from uuid import uuid4
from django.forms.models import model_to_dict


class MainFeed(APIView):

	def get (self, request):
		# 피드(게시물) 조회
		# 해당 아이디로 좋아요 & 북마크 boolean 조회

		email = request.session.get('email', None)
		if not email: # 유저정보없이 접속시
			return render(request, 'user/login.html')

		user = User.objects.filter(email=email).first() # 회원정보
		if not user:
			return render(request, 'user/login.html')

		# Feed(id) -> Like, Bookmark 조회
		feed_objects = Feed.objects.all().order_by("-id")

		feed_list = []
		for feed in feed_objects:
			feed_dict = model_to_dict(feed) # Feed 모델을 dict으로 변환 후 추가
			# User profile_image 검색
			feed_profile_image = User.objects.filter(email=feed.email).first().profile_image
			feed_dict['profile_image']  = feed_profile_image
			# Like 검색
			if Like.objects.filter(feed_id=feed.id, email=email).exists(): # True & False
				feed_dict['like']  = 'favorite'
				feed_dict['color'] = "red"
			else:
				feed_dict['like']  = 'favorite_border'
				feed_dict['color'] = "black"
			
			# Bookmark 검색
			if Bookmark.objects.filter(feed_id=feed.id, email=email).exists(): # True & False
				feed_dict['bookmark']  = 'turned_in'
			else:
				feed_dict['bookmark']  = 'turned_in_not'

			# comments 검색
			Comments = Comment.objects.filter(feed_id=feed.id).order_by("-id")
			if Comments.exists(): # True & False
				feed_dict['comment'] = Comments
			else:
				feed_dict['comment'] = None

			feed_list.append(feed_dict)

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