from django.db import models

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
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, to_field='name')
    # command description
    description = models.CharField(max_length=500)
    # Redirect URL
    redirect_url = models.CharField(max_length=150)
