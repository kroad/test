from django.shortcuts import render

# Create your views here.
import os
import mimetypes
import shutil
import cv2

from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from vals.serializer import UploadVideoSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from vals.models import Genre,UploadVideo
from uuid import UUID





class VideoCreateView(CreateAPIView):
    serializer_class = UploadVideoSerializer
    def create(self, request, *args, **kwargs):
        """defaultだとfileのurlを返すが、tokenを返すように変更"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {

            'token': str(serializer.instance.token),

        }
        response = Response(response_data, status=HTTP_201_CREATED, headers=headers)

        return response





class VideoDownloadView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        token = UUID(self.request.query_params.get('token'))
        
        '''magenta動かすとき
        genre = self.request.data['genre']
        
        mp4_path = main_test()
        '''
        mp4_path = os.path.dirname(os.path.abspath(__file__)) + '/mp4/pen.mp4'
        mp4_path = mp4_path.replace('\\','/')
        
        cap = cv2.VideoCapture(mp4_path)
        
        new_filename = str(token) + '.mp4'
        

        response = HttpResponse(content_type=mimetypes.guess_type(new_filename)[0] or 'application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={new_filename}'
        shutil.copyfileobj(cap, response)

        return response




        