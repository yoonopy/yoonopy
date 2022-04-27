from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from uuid import uuid4
from user.models import User
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
		profile_image = os.path.basename(request.data.get('profile_image'))
		user_id = request.data.get('user_id')
		email = request.data.get('email')

		Feed.objects.create(content=content, image=image, profile_image=profile_image, 
									user_id=user_id, email=email, like_count=0)

		return Response(status=200)


class LikeFeed(APIView): # 좋아요
	
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

class BookmarkFeed(APIView): # 북마크 추가
    	
	def post(self, request):
		
		feed_id  = request.data.get('feed_id')
		email    = request.data.get('email')
		boolean_bookmark = request.data.get('boolean_bookmark') # str으로 넘어옴

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


class CommentFeed(APIView): # 댓글 달기
    	
	def post(self, request):
		
		feed_id = request.data.get('feed_id')
		email   = request.data.get('email')
		user_id = request.data.get('user_id') 
		comment = request.data.get('comment')

		# Comment ok > db 저장
		Comment.objects.create(feed_id=feed_id,
							email=email,
							user_id=user_id,
							comment=comment
							)

		lately_id = Comment.objects.filter(feed_id=feed_id,
											email=email,
											comment=comment).order_by("-id").first()

		return Response(status=200, data={"message" : "댓글db저장 성공", "lately_id" : lately_id.id})


class DeleteFeed(APIView): # 피드 삭제
    	
	def post(self, request):
    	# 피드
		# 좋아요 
		# 북마크 
		# 댓글  삭제

		feed_id = request.data.get('feed_id')
		email   = request.data.get('email')
		user_id = request.data.get('user_id') 

		# 사용자와 피드주인 확인
		fedd_model = Feed.objects.filter(id=feed_id).first()

		print(fedd_model)
		print(fedd_model.email)
		if email != fedd_model.email:
			print (" 사용자 다름 ")
			return Response(status=200, data={"message":"삭제 권한이 없습니다.", "value":0})

		# -- 삭제 -- 
		fedd_model.delete()
		like_model = Like.objects.filter(feed_id=feed_id)
		if like_model.exists():
			like_model.first().delete()
		bookmark_model = Bookmark.objects.filter(feed_id=feed_id)
		if bookmark_model.exists():
			bookmark_model.first().delete()
		comment_model = Comment.objects.filter(feed_id=feed_id)
		if comment_model.exists():
			comment_model.first().delete()

		if os.path.exists(os.path.join(MEDIA_ROOT,fedd_model.image)):
			os.remove(os.path.join(MEDIA_ROOT,fedd_model.image))

		return Response(status=200, data={"message":"피드 삭제 성공","value" : 1})


class DeleteComment(APIView): # 댓글 삭제
    	
	def post(self, request):
		
		model_id = request.data.get('model_id')
		feed_id = request.data.get('feed_id')
		email   = request.data.get('email')
		user_id = request.data.get('user_id') 

		model = Comment.objects.filter(id=model_id).first()

		if email != model.email:
			print (" 사용자 다름 ")
			return Response(status=200, data={"message":"삭제 권한이 없습니다.", "value":0})

		print (" 사용자 같음 ")
		model.delete()

		return Response(status=200, data={"message":"댓글 삭제 성공","value" : 1})