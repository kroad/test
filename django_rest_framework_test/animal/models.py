from django.db import models

# Create your models here.
class User(models.Model):
    """ログイン画面のmodel"""
    name = models.CharField(max_length=32)
    pas = models.CharField(max_length=32)
    
    def __repr__(self):
        # 主キーとnameを表示させて見やすくする
        # ex) 1: Alice
        # pk: Primary Key
        return f'{self.pk}:{self.name}'
        
    __str__ = __repr__  # __str__にも同じ関数を適用    
    

class Output(models.Model):
    """サービスの核の部分"""
    title = models.CharField(max_length=64)
    input_body = models.CharField(max_length=128)
    output_body = models.TextField()
    # auto_now_add: インスタンスを作成(DBにINSERT)する度に更新される。DefaultではFalseになっている。
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now: モデルインスタンスを保存する度に現在の時間で更新される。DefaultではFalseになっている。
    updated_at = models.DateTimeField(auto_now=True)
    
    """Δmodels.ForeignKeyΔ
    ・外部キー制約と言って、違うテーブルの情報を参照したい場合に使うテーブルのリレーション方法の1つ。 設定するとテーブル同士が一対多の関係を持つ
    ・テーブル: 表のようなもの
    ・Userを参照している（User一つに対して多数のOutputsがある構造）
    ・on_delete: 参照するオブジェクトが削除されたときに、それと紐づけられたオブジェクトも一緒に削除するのか、それともそのオブジェクトは残しておくのかを設定するもの
    ・models.CASCADE: 削除するオブジェクトに紐づいたオブジェクトを全て削除する（Userが削除されるとOutputsも全て削除される)
    """
    author = models.ForeignKey(User, related_name='Outputs', on_delete=models.CASCADE)
    
    def __repr__(self):
        # 主キーとtitleを表示させて見やすくする
        # ex) 1: 「孫氏の兵法」から学んだこと
        # pk: Primary Key
        return f'{self.pk}:{self.title}'
        
    __str__ = __repr__  # __str__にも同じ関数を適用    
    
    