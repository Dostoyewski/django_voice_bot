from django.db import models
from django.urls import reverse

LANG = (
    (0, "Русский"),
    (1, "English"),
    (2, "Deutsch"),
    (3, "Francias")
)


# TODO Make decorator to register Bot for some page
class Bot(models.Model):
    """
    Bot model
    Used to make voice bot
    """
    # Bot descriprion, optional
    description = models.CharField(max_length=1000, blank=True)
    # Language selection
    language = models.IntegerField(choices=LANG)
    # Name
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name + ", " + "Language: " + self.get_language()

    def get_language(self):
        """
        Returns language code
        :return: lang code
        """
        if self.language == 0:
            return 'ru-RU'
        elif self.language == 1:
            return 'en-US'
        elif self.language == 2:
            return 'de-DE'
        elif self.language == 3:
            return 'fr-FR'


class Command(models.Model):
    """
    Command class
    Needs to be attached to bot
    """
    # Link to bot object
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, to_field='name',
                            help_text="bot that will execute the command")
    # command description
    description = models.CharField(max_length=500)
    # Redirect URL
    redirect_url = models.CharField(max_length=150,
                                    help_text="Link or name of the page on the site to be redirected to. "
                                              "For an external page — it must start with 'www', "
                                              "otherwise the link will be recognized as the template name.")
    # Words, that will used to execute command
    # Should be separated by comma (',')
    trigger_words = models.CharField(max_length=1000, default="",
                                     help_text="Code words for executing the command. "
                                               "Sets of code words must be separated by a comma, "
                                               "and code words in the set must "
                                               "be separated by a space.")

    def get_triggers(self):
        """
        Returns trigger words
        :return:
        """
        return self.trigger_words.split(sep=',')

    def process_redirect(self):
        """
        Redirects to page
        :return:
        """
        if self.redirect_url[0:3] == "www":
            return "https://" + self.redirect_url
        elif self.redirect_url[0:3] == "htt":
            return self.redirect_url
        else:
            return reverse(self.redirect_url)

    def check_msg(self, msg):
        """
        checks, if msg is equals to trigger words
        :param msg: recognized message
        :return: bool
        """
        words = self.trigger_words.split(sep=',')
        for word in words:
            if msg in word:
                return True
        return False
