from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from stagram.settings import MEDIA_ROOT
from uuid import uuid4
import os


class Login(APIView):
    
	def get(self, request):
		print("\n 로그인 페이지")
		return render(request, "user/login.html")

	def post(self, request):
    	
		email = request.data.get('email')
		password = request.data.get('password')

		# 이메일 존재유무
		# password 확인
		if not User.objects.filter(email=email).exists():
			return Response(status=500, data=dict(message='사용자 정보가 잘못되었습니다.'))

		user = User.objects.filter(email=email).first() # 유저정보
		if not check_password(password, user.password): # password 확인
			return Response(status=500, data=dict(message="사용자 정보가 잘못되었습니다."))

		## 세션 넣기
		request.session['email'] = email

		return Response(status=200, data=dict(message="로그인에 성공했습니다."))


class Join(APIView):

	def get(self, request):
		print("\n 회원가입 페이지")
		return render(request, "user/join.html")

	def post(self, request):
    		
		email = request.data.get('email')
		name = request.data.get('name')
		user_id = request.data.get('user_id')
		password = request.data.get('password')

		# 이메일 존재유무
		# 사용자이름 존재유무
		if User.objects.filter(email=email).exists():
			return Response(status=500, data=dict(message='이메일 주소가 이미 존재합니다.'))
		if User.objects.filter(user_id=user_id).exists():
			return Response(status=500, data=dict(message="사용자 이름이 이미 존재합니다."))

		# insert
		User.objects.create(email=email,
							name=name,
                            user_id=user_id,
							password=make_password(password),
							)

		return Response(status=200, data=dict(message="회원가입에 성공했습니다."))


class Logout(APIView):

	def get(self, request):
		request.session.flush() # 세션삭제
		return render(request, "user/login.html")


class UpdateProfile(APIView):
    
	def post(self, request):
    	
		print ("Sdfsfsdfasfeasfesf")
		email = request.session.get('email', None) # 사용자확인
		if not email:
			return render(request, 'user/login.html')

		user = User.objects.filter(email=email).first() # 사용자정보
		if not user:
			return render(request, 'user/login.html')

		file = request.FILES['file']
		if not file:
			return render(status=500)
		
		ext  = os.path.splitext(str(file.name))[1] # 확장자
		image_name = uuid4().hex + ext
		save_path = os.path.join(MEDIA_ROOT, image_name)

		with open(save_path, 'wb+') as destination: # 파일쓰기
			for chunk in file.chunks():
				destination.write(chunk)

		user.profile_image = image_name # 이미지 바꾸기
		user.save()

		return Response(status=200, data=dict(image_name=image_name))