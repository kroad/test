
"""rest_framework.routers"""
"""
・ViewSetを使う場合、routerを使う
・逆にrouterを使えるのはViewSetのみ
"""

from rest_framework import routers
from .views import UserViewSet, OutputViewSet

# DefaultRouter: Router のルート画面にアクセスしたときに API のリンク一覧を見せてくれる
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'outputs', OutputViewSet)