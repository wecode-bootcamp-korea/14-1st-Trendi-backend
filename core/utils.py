import jwt
import bcrypt
import re

from django.htp import JsonResponse

from my_settings import SECRET, ALGORITHM
from user.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get('Authorization', None)
            payload      = jwt.decode(token, SECRET['secret'], algorithm=ALGORITHM['algorithm'])
            user         = User.objects.get(id=payload['user_id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({"MESSAGE": "INVALID_TOKEN"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)
        return func(self, request, *args, **kwargs)
    return wrapper

def get_hashed_pw(password):
    return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")

def validate_password(password):
    return re.match('(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[`~!@#$%^&*_+-=]).{8,20}', password)

def validate_nick_name(nick_name):
    return re.match('^[a-zA-Z0-9]{1,20}$', nick_name)

def validate_user_name(user_name):
    return re.match('^[a-z가-힣A-Z0-9]{1,20}$', user_name)

def validate_email(email):
    return re.match('^[a-zA-Z0-9_+.-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z0-9]+$', email)