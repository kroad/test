# django_filters: 
import django_filters

"""ViewSetを使ったview.pyの記述"""
"""
・普通のviewでは、更新、削除などを1つ1つ定義しなければいけないが、それらをまとめてセットにして使える
・ただし、urls.pyでrouterを使わないと動かない
"""
from rest_framework import viewsets, filters

from .models import User, Output
from .serializer import UserSerializer, OutputSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OutputViewSet(viewsets.ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer