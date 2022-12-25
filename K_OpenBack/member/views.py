from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import time

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.utils.decorators import method_decorator
from .models import UserDB
from .storages import FileUpload, s3_client

# member/views.py

# http://127.0.0.1:8000/member/join/ 요청시 호출되는 함수

# csrf e
@method_decorator(csrf_exempt, name='dispatch')
def join(request) :
    if request.method != "POST" :
        return HttpResponse("post 방식이 아닙니다.", status=status.HTTP_200_OK)
      # return render(request,"member/join.html")
    else: # POST 방식
       member = UserDB(id=request.POST["id"],\
                    passwd=request.POST["passwd"],\
                    name=request.POST["name"],
                    email=request.POST["email"],)
       member.save() #insert 문장 실행.
       return HttpResponse("회원가입 성공", status=status.HTTP_200_OK)
       # return HttpResponseRedirect("../login/")

@method_decorator(csrf_exempt, name='dispatch')
def login(request) :
    print("1:",request.session.session_key)
    if request.method != "POST" :
        return HttpResponse("post 방식이 아닙니다.", status=status.HTTP_200_OK)
       # return render(request,"member/login.html")
    else :
       inputId=request.POST["id"]
       inputPasswd=request.POST["passwd"]
       try :
           #입력된 id값으로 Member 객체에서 조회
           member = UserDB.objects.get(id=inputId) #select 문장 실행
       except :  #db에 아이디 정보가 없을 때
           context = {"msg":"아이디를 확인하세요."}
           return HttpResponse("아이디가 틀립니다.", status=status.HTTP_200_OK)
           # return render(request,"member/login.html",context)
       else :  #정상적인 경우. 아이디 정보가 조회된 경우
           if member.passwd == inputPasswd :  #로그인 정상
              time.sleep(1)
              print("2:",request.session.session_key)
              request.session["login"] = inputId  #session 객체에 login 등록.
              return HttpResponse("로그인 성공", status = status.HTTP_200_OK)
              # return HttpResponseRedirect("../main")
           else :  #비밀번호 오류
               context = {"msg":"비밀번호가 틀립니다.","url":"../login/"}
               return HttpResponse("비밀번호가 틀립니다.", status=status.HTTP_200_OK)
               # return render(request,"alert.html",context)

# http://127.0.0.1:8000/member/s3Upload/ 요청시 호출되는 함수
@method_decorator(csrf_exempt, name='dispatch')
def s3Upload(request) :
    file = request.FILES['filename']
    profile_image_url = FileUpload(s3_client).upload(file)
    return HttpResponse(profile_image_url, status=status.HTTP_200_OK)

