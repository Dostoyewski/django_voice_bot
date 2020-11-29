import ast
from random import randrange

import requests
from django.db import models

LANG = (
    (0, "Русский"),
    (1, "English"),
    (2, "Deutsch"),
    (3, "Francias")
)

FULL = (
    (0, "Speech only first trigger"),
    (1, "Speech all triggers")
)

API_URL = (
    (0, "Message will be set default"),
    (1, "Message will be updated using API URL")
)


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
    # Speech full commands triggers
    speech_full = models.IntegerField(choices=FULL)
    # Bot success messages, should be splitten with comma
    success_messages = models.CharField(max_length=500, help_text="Bot success messages, "
                                                                  "should be splitten with comma")
    # Bot failure messages, should be splitten with comma
    failure_messages = models.CharField(max_length=500, help_text="Bot failure messages, "
                                                                  "should be splitten with comma")

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

    def get_success_message(self):
        """
        Returns random success message
        :return:
        """
        wset = self.success_messages.split(sep=',')
        return wset[randrange(len(wset))]

    def get_failure_message(self):
        """
        Returns random failure message
        :return:
        """
        wset = self.failure_messages.split(sep=',')
        return wset[randrange(len(wset))]


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
    # execution custom message
    message = models.CharField(max_length=500, default="", blank=True,
                               help_text="Custom message that will be displayed when the"
                                         " command is executed. Leave empty for the "
                                         "default option")
    # callback URL to updating message
    api_url = models.CharField(max_length=150, help_text="API URL to update message", default="", blank=True)
    # API using flag
    api_flag = models.IntegerField(choices=API_URL, default=0, help_text="Flag that will handle message")
    # Header that will be used to extract data from api response
    api_header = models.CharField(max_length=200, default="", blank=True,
                                  help_text="API header, "
                                            "that will be used to extract data")
    # Request headers
    requests_headers = models.CharField(max_length=500, default="", blank=True, help_text="request headers,"
                                                                                          "should be written as json")

    def process_API(self):
        """
        Loads data from API and updates message
        :return:
        """
        if self.api_flag:
            response = requests.get(self.api_url, headers=self.requests_headers)
            if response.status_code == 200:
                self.message = ast.literal_eval(response.text.replace("\r\n", ' '))[self.api_header]

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
        else:
            return self.redirect_url

    def check_msg(self, msg):
        """
        checks, if msg is equals to trigger words
        :param msg: recognized message
        :return: bool
        """
        words = self.trigger_words.split(sep=',')
        for word in words:
            if msg.lower() in str(word).lower():
                return True
        return False

    def get_message(self):
        """
        return success message
        :return:
        """
        self.process_API()
        if self.message == "":
            bot = Bot.objects.get(name=self.bot)
            return bot.get_success_message()
        else:
            return self.message
