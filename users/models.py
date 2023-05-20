"""
Module for defining user specific models.

Models:
    - WatchList model: Model which is in one-to-one relation with
        django user model containing information about user specific
        symbols list.

        Attributes:
            user: Field which points to corresponding user model
                with which it is in one-to-one relation.
            symbols: Field which stores the names of user's
                chosen stock symbols. Like MSFT, GOOG and etc.
                Note: Currently the max length of symbols field is 5
                because of aplha_avantage's free api limitation.

"""

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


class WatchList(models.Model):
    """
    WatchList Model is defined as one-to-one relation model with django's
    user model to extend the django's basic user model. So that the symbols
    belongs to a particular user can be stored along with its user model.

    Attributes:
        user: Field which points to corresponding user model
            with which it is in one-to-one relation.
        symbols: Field which stores the names of user's
            chosen stock symbols. Like MSFT, GOOG and etc.
            Note: Currently the max length of symbols field is 5
            because of aplha_avantage's free api limitation.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    symbols = models.JSONField(default=list)


@receiver(post_save, sender=User)
def create_user_watchlist(sender, instance, created, **kwargs):
    """Function to generate WatchList object whenever a user
    object is created.

    Args:
        sender (Type[Model]): A model from which create signal is generated.
        instance (Model): A model instance which needs to be store.
        created (bool): Wether instance is created or not.
    """

    if created:
        WatchList.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_watchlist(sender, instance, **kwargs):
    """Function to update the WatchList object whenever a user
    object is updated.

    Args:
        sender (Type[Model]): A model from which update signal is generated.
        instance (Model): A model instance which needs to be store.
    """

    instance.watchlist.save()
