# django_voice_bot
Package for django support bot with speech recognition and voice commands.<br>

Installation
------------

To install it, simply: ::
    
    pip install django-voice-bot


Quick start
-----------

1. Add "voice-bot" to your INSTALLED_APPS setting like this ::

    INSTALLED_APPS = [
        ...
        'voice-bot',
    ]

2. Include the bot URLconf in your project urls.py like this ::

    path('/', include('voice-bot.urls')),

3. Run ``python manage.py migrate`` to create the voice-bot models.

4. To connect the bot to the view, you must specify the decorator ```@add_bot(bot_name='BOT_NAME')``` before the view.<br>
5. Then insert to view template following code ::

    {% include "voice-bot/bot_include.html" %}
 
6. Modify your function as follows ::

    @add_bot(bot_name='BOT_NAME')
    def attached_function(request, **kwargs):
        ...
        return render(request, 'your_template_name.html', {"commands": kwargs['commands'],
                                                           "bot_name": kwargs['bot_name']})

7. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a voice-bot (you'll need the Admin app enabled).

5. Setup your bot
In the admin panel, you need to set the bot's language, name, and messages about successful and unsuccessful command execution.<br>
The```speech_full``` flag will play all trigger phrases for all bot commands when activated.<br>
Then you need to set commands for the bot.<br> Parameters:<br> ```description``` — description of the bot;<br> ```redirect_url``` — URL that will be redirected to when executing the command, can be global.<br> ```trigger_words``` - the words that trigger the command must be separated by commas.<br> ```message``` — the message that will be voiced when the command is executed.<br> ```api_url``` - link to the url from which data will be uploaded.<br> ```api_flag``` — when activated, the default message will be replaced with the one received from the API.<br> ```api_header``` - the header from which the new message will be written.<br> ```request_headers``` - request headers.
