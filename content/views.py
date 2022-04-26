from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from uuid import uuid4
from .models import Feed, Like, Bookmark, Comment
from stagram.settings import MEDIA_ROOT


class UploadFeed(APIView):
    	
	def post(self, request):

		file = request.FILES['file']
		ext  = os.path.splitext(str(file.name))[1]  # 확장자

		uuid_name = uuid4().hex + ext # 고유id
		save_path = os.path.join(MEDIA_ROOT, uuid_name)

		# 파일쓰기
		with open(save_path, 'wb+') as f:
			for chunk in file.chunks():
				f.write(chunk)

		# data.get 로 파일 받기
		content = request.data.get('content')
		image   = uuid_name
		profile_image = request.data.get('profile_image')
		user_id = request.data.get('user_id')

		Feed.objects.create(content=content, image=image,
		                    profile_image=profile_image, user_id=user_id, like_count=0)

		return Response(status=200)


class LikeFeed(APIView):
	
	def post(self, request):
		
		feed_id      = request.data.get('feed_id')
		email        = request.data.get('email')
		boolean_like = request.data.get('boolean_like') # str
		like_count   = int(request.data.get('like_count'))

		# like ok > db 저장
		# like no > db 삭제
		like_model = Like.objects.filter(feed_id=feed_id, email=email)
		message = ''
		if boolean_like == 'true':
			if not like_model.exists():
				message = '좋아요 추가'
				like_count += 1
				Like.objects.create(feed_id=feed_id,email=email)
		else: # no like & 테이블에 존재
			if like_model.exists():
				message = '좋아요 삭제'
				like_count -= 1
				like_model.delete()

		# 저장
		feed_model = Feed.objects.filter(id=feed_id).first()
		feed_model.like_count = like_count
		feed_model.save()

		return Response(status=200, data={"message" : message})

class BookmarkFeed(APIView):
    	
	def post(self, request):
		
		feed_id  = request.data.get('feed_id')
		email    = request.data.get('email')
		boolean_bookmark = request.data.get('boolean_bookmark') # str으로 넘어옴

		print ('\n\n')
		print (feed_id)
		print (email)
		print (type(boolean_bookmark), boolean_bookmark)

		# bookmark ok > db 저장
		# bookmark no > db 삭제
		bookmark_model = Bookmark.objects.filter(feed_id=feed_id,email=email)
		message = ''
		if boolean_bookmark == 'true':
			if not bookmark_model.exists():
				message = '북마크 추가'
				Bookmark.objects.create(feed_id=feed_id,email=email)
		else: # no like & 테이블에 존재
			if bookmark_model.exists():
				message = '북마크 삭제'
				bookmark_model.delete()

		return Response(status=200, data={"message" : message})


class CommentFeed(APIView):
    	
	def post(self, request):
		
		feed_id = request.data.get('feed_id')
		email   = request.data.get('email')
		user_id = request.data.get('user_id') 
		comment = request.data.get('comment')

		print ('\n')
		print (feed_id)
		print (email)
		print (user_id)
		print (comment)
		
		# Comment ok > db 저장
		Comment.objects.create(feed_id=feed_id,
							email=email,
							user_id=user_id,
							comment=comment
							)

		return Response(status=200, data={"message" : "댓글db저장 성공"})