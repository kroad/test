from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from vals import views as v



urlpatterns = [

    path('create/', v.VideoCreateView.as_view()),

    path('get/', v.VideoDownloadView.as_view()),

]