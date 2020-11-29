import os

import speech_recognition as sr
from django.http import JsonResponse
from django.shortcuts import render
from speech_recognition import UnknownValueError

from .decorators import add_bot
from .models import Command, Bot


def upload(request):
    """
    Recognizes speech and make redirects
    :param request: POST XMLHttpRequest with speech file to process
    :return: url to page corresponding command or error message
    """
    bot_name = request.META['HTTP_BOTID']
    bot = Bot.objects.get(name=bot_name)
    # obviously handle correct naming of the file and place it somewhere like media/uploads/)
    filename = "name" + ".wav"
    uploadedFile = open(filename, "wb")
    # the actual file is in request.body
    uploadedFile.write(request.body)
    uploadedFile.close()
    # put additional logic like creating a model instance or something like this here
    r = sr.Recognizer()
    harvard = sr.AudioFile(filename)
    with harvard as source:
        audio = r.record(source)
    try:
        msg = r.recognize_google(audio, language=bot.get_language())
        os.remove(filename)
        msg = str(msg).lower()
        commands = Command.objects.filter(bot=bot_name)
        for command in commands:
            if command.check_msg(msg):
                url = command.process_redirect()
                print(url)
                return JsonResponse({'url': url, 'message': bot.get_success_message()})
        return JsonResponse({'url': '/', 'message': bot.get_failure_message()})
    except UnknownValueError:
        return JsonResponse({'url': '/', 'message': bot.get_failure_message()})


@add_bot(bot_name='Simple Bot')
def home(request, **kwargs):
    """
    Main page with active bot
    :param request:
    :return: render with main page
    """
    return render(request, 'base.html', {"commands": kwargs['commands'],
                                         "bot_name": kwargs['bot_name']})


def test(request):
    """
    Main page with active bot
    :param request:
    :return: render with main page
    """
    return render(request, 'test.html')
