from django.contrib import admin

from .models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'first_name',
        'last_name',
        'date_birth',
        'tg_id'
    ]

    readonly_fields = ['tg_id']
