from rest_framework import serializers

from .models import User, Output


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'pas')


class OutputSerializer(serializers.ModelSerializer):
    # authorのserializerを上書き
    # 今まで author:1 となっていたのが、author: {'name':     ,'pas':     } の形にできるようになる
    author = UserSerializer()    
    
    class Meta:
        model = Output
        # updated_at: サーバー側で見る情報なのでいらない(APIとして出力したいわけではない)
        fields = ('title', 'input_body', 'output_body','created_at',  'author')