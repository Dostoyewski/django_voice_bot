from django.contrib import admin

from voice_bot.models import Bot, Command


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('description', 'language', 'name',)
    search_fields = ['name']


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ['bot', 'redirect_url', 'description']
    search_fields = ['bot', 'redirect_url']
    fieldsets = (
        (None, {
            'fields': ('description', 'bot', 'redirect_url', 'trigger_words', 'message')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('api_flag', 'api_url', 'api_header'),
        }),
    )
