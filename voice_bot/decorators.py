from .models import Command


def add_bot(bot_name):
    """
    Decorator to attach bot
    :param bot_name: name of bot attach it to template
    :return: function
    """

    def wrap(view):
        def wrapped(request, *args, **kwargs):
            commands = Command.objects.filter(bot=bot_name)
            kwargs['commands'] = process_text(commands)
            kwargs['bot_name'] = bot_name
            return view(request, *args, **kwargs)

        return wrapped

    return wrap


def process_text(commands):
    """
    Constructs detailed text with commands info
    :param commands:
    :return: beautified commands info
    """
    text = "Мои команды: "
    for command in commands:
        text += command.description + ", " + " для выполнения произнесите "
        text += command.trigger_words.split(sep=',')[0] + " ; "
    return text
