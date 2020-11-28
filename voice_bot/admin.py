from django.contrib import admin

from voice_bot.models import Bot, Command


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('description', 'language', 'name',)
    search_fields = ['name']


@admin.register(Command)
class BotAdmin(admin.ModelAdmin):
    list_display = ('description', 'bot', 'redirect_url',)
    search_fields = ['bot', 'redirect_url']
