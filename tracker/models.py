from django.db import models

from shared.models import AbstractModel

from .values import DefaultModelValues


class Repository(AbstractModel):
    """
    A model representing a repository, including its name, author, and link.

    Attributes:
    - name (CharField): The name of the repository with a max length defined by DefaultModelValues.
    - author (CharField): The author of the repository with a max length defined by DefaultModelValues.
    - link (URLField): A URL to the repository with a max length defined by DefaultModelValues.

    Inherits from:
    - AbstractModel: A shared abstract model providing common fields or methods.

    Methods:
    - __str__: Returns a string representation of the repository in the format 'author/name'.
    """

    # TODO: add validators to check if the repository exists
    name = models.CharField(max_length=DefaultModelValues.name_max_length)
    author = models.CharField(max_length=DefaultModelValues.author_max_length)
    link = models.URLField(max_length=DefaultModelValues.link_max_length)

    def __str__(self) -> str:
        """
        Returns a string representation of the repository in the format 'author/name'.
        :return: str
        """
        return f"{self.author}/{self.name}"
