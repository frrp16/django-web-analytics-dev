from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, OutstandingToken
from rest_framework_simplejwt.exceptions import TokenError


from ..serializers import UserSerializer
from ..api import get_dataset_monitorlog
from ..models import Dataset

def get_user_from_token(token):
    try:                
        user_id = AccessToken(token).get('user_id')
        return User.objects.get(id=user_id)
    except TokenError as e:
        raise e        

def register_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            if new_user:
                refresh = RefreshToken.for_user(new_user)
                return {'refresh': str(refresh), 'access': str(refresh.access_token)}, 201
        return serializer.errors, 400
    except Exception as e:
        return str(e), 500

def logout_user(request):
    refresh_token = request.data["refresh"]
    try:
        token = RefreshToken(refresh_token)
        outstanding_token = OutstandingToken.objects.filter(token=token).first()
        if outstanding_token:
            outstanding_token.delete()
            return "Logout", 205
        else:
            return "Token not found", 400
    except Exception as e:
        return str(e), 500

def get_user_serialize(request):
    token = request.headers.get('Authorization').split()[1]
    try:
        user_instance = get_user_from_token(token)
        serializer = UserSerializer(user_instance)
        for datasets in serializer.data['datasets']:
            datasets['monitor_logs'] = get_dataset_monitorlog(datasets['id'])                            
        return serializer.data
    except Exception as e:
        raise Exception(e)