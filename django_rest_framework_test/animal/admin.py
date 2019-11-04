from django.contrib import admin

# Register your models here.
from .models import User, Output


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Output)
class Output(admin.ModelAdmin):
    pass
