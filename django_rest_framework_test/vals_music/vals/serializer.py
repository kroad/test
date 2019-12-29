from rest_framework import serializers
from vals.models import UploadVideo



class UploadVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadVideo
        # fields以外は自動で埋まる
        fields = ('file',)
        
