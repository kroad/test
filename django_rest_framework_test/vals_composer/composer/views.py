from django.shortcuts import render

# Create your views here.
import os
import glob
import random
import mimetypes
import pandas as pd

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from composer.serializer import UploadVideoSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from composer.models import UploadVideo
from uuid import UUID

from .parts_magenta import main_test_v8

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
        token = self.get_token()
        obj = self.get_object()
        file_path = obj.file.path
        
        score = 12
        #score = request.data['genre']
        
        music_database_path = os.path.dirname(os.path.abspath(__file__)) + '/parts_magenta/main_test_parts/music_database/'

        song_path = random.choice([i for i in glob.glob(music_database_path + '*') if f'{score}_' in i])
        
        song = song_path.split('/')[-1]

        real_mid = song_path + f'/{song}_melody/{song}_melody.mid'
        
        backing_dir = song_path + f'/{song}_back'
        
        csv = pd.read_csv(f'{song_path}/{song}.csv')
        
        mp4_path_response = main_test_v8.main(
            token_name = str(token),
            real_midi_name =  real_mid,
            primer_melody_list = csv.loc[0]['primer_mel'],
            chord_name = csv.loc[0]['backing_chords'],
            backing_dir = backing_dir,
            mp4_path = file_path,
            bpm = csv.loc[0]['bpm'],
            score = score)
        
        filename = f'{token}.mp4'        

        with open(mp4_path_response, 'rb') as mp4:
            response = HttpResponse(mp4.read(), content_type=mimetypes.guess_type(filename)[0] or 'application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={filename}'
        
        return response
    
    
    def get_token(self):
        token = UUID(self.request.query_params.get('token'))
        return token
    
    def get_object(self):
        token = self.get_token()
        obj = get_object_or_404(UploadVideo, token=token)
        return obj