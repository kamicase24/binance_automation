"""Django models utilities"""

from django.db import models


class BinanceAutomationModel(models.Model):
    """
    utilitario
    """
    objects: models.Manager()
    DoesNotExist: models.ObjectDoesNotExist
    """
    BinanceAutomationModel It is a model that provides information
    on date and creation as well as the update of a field
    in a database channeled by the django model.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created',
        null=True
    ) # 6.00  6.06
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified',
        null=True
    )

    class Meta:
        """Meta option."""
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created','-modified']
