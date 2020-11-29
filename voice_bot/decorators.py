from .models import Command, Bot


def add_bot(bot_name):
    """
    Decorator to attach bot
    :param bot_name: name of bot attach it to template
    :return: function
    """

    def wrap(view):
        def wrapped(request, *args, **kwargs):
            commands = Command.objects.filter(bot=bot_name)
            bot = Bot.objects.get(name=bot_name)
            kwargs['commands'] = process_text(commands, bot.speech_full)
            kwargs['bot_name'] = bot_name
            return view(request, *args, **kwargs)

        return wrapped

    return wrap


def process_text(commands, speech_full):
    """
    Constructs detailed text with commands info
    :param commands: commands queryset
    :param speech_full: if True will speech all triiger words
    :return: beautified commands info
    """
    text = "Мои команды: "
    for command in commands:
        text += command.description + ", " + " для выполнения произнесите "
        text += command.get_triggers()[0]
        if speech_full:
            wsets = command.get_triggers()
            for i, wset in enumerate(wsets):
                if i != 0:
                    text += " или " + wset
        text += " ; "
    return text
