from dataclasses import dataclass


@dataclass(frozen=True)
class DefaultModelValues:
    """
    A data class to store default maximum length values for various fields in models.

    Attributes:
    - name_max_length (int): The maximum allowed length for the 'name' field. Default is 255.
    - author_max_length (int): The maximum allowed length for the 'author' field. Default is 255.
    - link_max_length (int): The maximum allowed length for the 'link' field. Default is 255.

    This class is immutable, so its values cannot be modified after instantiation.
    """

    name_max_length: int = 255
    author_max_length: int = 255
    link_max_length: int = 255
