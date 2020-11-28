import os

import speech_recognition as sr
from django.shortcuts import render, redirect


def upload(request):
    """
    Recognizes speech and make redirects
    :param request: POST XMLHttpRequest with speech file to process
    :return: redirect to page corresponding command or error message
    """
    customHeader = request.META['HTTP_MYCUSTOMHEADER']

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
    msg = r.recognize_google(audio, language='ru-RU')
    os.remove(filename)
    print(msg)
    return redirect('/')


def home(request):
    """
    Main page with active bot
    :param request:
    :return: render with main page
    """
    return render(request, 'base.html', {"commands": "Привет"})
