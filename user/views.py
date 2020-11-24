import json
import bcrypt
import jwt

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from my_settings      import SECRET, ALGORITHM
from .models          import User
from core.utils       import get_hashed_pw, validate_email, validate_password, validate_nick_name, validate_user_name

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email     = data["email"]
            user_name = data["user_name"]
            nick_name = data["nick_name"]
            password  = data["password"]

            if not validate_nick_name(nick_name):
                return JsonResponse({'message':'INVALID_NICK_NAME'}, status = 400)
            if not validate_password(password):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status = 400)
            if not validate_email(email):
                return JsonResponse({'message':'INVALID_EMAIL'}, status = 400)
            if not validate_user_name(user_name):
                return JsonResponse({'message':'INVALID_USER_NAME'}, status = 400)

            if User.objects.filter(
                Q(email     = email) |
                Q(nick_name = nick_name)
                ): 
                return JsonResponse({"MESSAGE" : "DUPLICATED_INFORMATION"}, status = 400)
            User.objects.create(
                email     = email,
                user_name = user_name,
                nick_name = nick_name,
                password  = get_hashed_pw(password)
                )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status = 201)
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)

class SignUpIdView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            nick_name = data["id"]
            if not validate_nick_name(nick_name):
                return JsonResponse({'message':'INVALID_NICK_NAME'}, status = 400)

            if User.objects.filter(nick_name = nick_name).exists(): 
                return JsonResponse({"MESSAGE" : "DUPLICATED_INFORMATION"}, status = 400)
            return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)

class SignUpEmailView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email = data["email"]
            if not validate_email(email):
                return JsonResponse({'message':'INVALID_EMAIL'}, status = 400)

            if User.objects.filter(email = email).exists(): 
                return JsonResponse({"MESSAGE" : "DUPLICATED_INFORMATION"}, status = 400)
            return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)

class LogInView(View):
    def post(self, request):
        data      = json.loads(request.body)
        password  = data['password']
        nick_name = User.objects.filter(nick_name=data['nick_name'])
        if 'nick_name' not in data or 'password' not in data:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)

        if User.objects.filter(nick_name=data['nick_name']).exists():
            user = User.objects.get(nick_name=data['nick_name'])
            if bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
                token = jwt.encode({'user_id' : user.id}, SECRET['secret'], algorithm=ALGORITHM['algorithm']).decode('UTF-8')
                return JsonResponse({'TOKEN' : token, 'user_name' : user.user_name, 'id':user.nick_name}, status = 200)
            return JsonResponse({"MESSAGE" : "INVALID_USER"}, status = 401)
        return JsonResponse({"MESSAGE" : "NO_EXIST_USER"}, status = 400)


