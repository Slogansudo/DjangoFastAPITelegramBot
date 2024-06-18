import uuid
from django.db import models


class SaveMediaFile(object):

    def employee(instance, filename):
        image_extension = filename.split('.')[-1]
        return f'employees/{uuid.uuid4()}.{image_extension}'

    def product(instance, filename):
        image_extension = filename.split('.')[-1]
        return f'product/{uuid.uuid4()}.{image_extension}'

    def category(instance, filename):
        image_extension = filename.split('.')[-1]
        return f'category/{uuid.uuid4()}.{image_extension}'


class PriceType(models.TextChoices):
    USD = '$', '$'
    SUM = "so'm", "SO'M"
