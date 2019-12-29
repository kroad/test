from django.contrib import admin

# Register your models here.
from .models import Genre, UploadVideo

@admin.register(Genre)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UploadVideo)
class UserAdmin(admin.ModelAdmin):
    pass

