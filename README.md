# django_voice_bot
Package for django support bot with speech recognition and voice commands.<br>

Installation
------------

To connect the bot to the view, you must specify the decorator ```@add_bot(bot_name='BOT_NAME')``` before the view.<br>
In the admin panel, you need to set the bot's language, name, and messages about successful and unsuccessful command execution.<br>
The```speech_full``` flag will play all trigger phrases for all bot commands when activated.<br>
Then you need to set commands for the bot.<br> Parameters:<br> ```description``` — description of the bot;<br> ```redirect_url``` — URL that will be redirected to when executing the command, can be global.<br> ```trigger_words``` - the words that trigger the command must be separated by commas.<br> ```message``` — the message that will be voiced when the command is executed.<br> ```api_url``` - link to the url from which data will be uploaded.<br> ```api_flag``` — when activated, the default message will be replaced with the one received from the API.<br> ```api_header``` - the header from which the new message will be written.<br> ```request_headers``` - request headers.
