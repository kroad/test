from django.db import models

# Create your models here.
import uuid,random


class Genre(models.Model):
    Rock_Hard = 1
    Rock_Soft = 2
    Pops_Hard = 3
    Pops_Soft = 4
    Classic = 5
    
    genre = models.IntegerField(editable=False)
    
    
    
def filename_manager(instance, filename):
    instance.filename = filename
    return str(uuid.uuid4())           # 4はUUIDのバージョン。strにすることで文字列として取得できる


class UploadVideo(models.Model):
    """アップロードされた動画(ファイル)を紐づけるモデル"""
    """
    file.nameでfile名を保存するが重複する場合末尾を変えてしまう。
    file.name自体はuuidに変更する
    なので、filenameを別で定義して、そこにfile.nameを保存する
    """

    # userの紐づけをするなら
    # user = models.ForeignKey(to=User,...)
    file = models.FileField(max_length=256, upload_to=filename_manager)
    filename = models.CharField(max_length=256, blank=True)
    # tokenを自動で作成する
    # 二度使う場合はtokenで呼び出す
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    uploaded_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        """:return file URL"""
        return self.file.url