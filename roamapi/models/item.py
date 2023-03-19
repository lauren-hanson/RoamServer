from django.db import models

class Item(models.Model):

    name = models.CharField(max_length = 50)
    category = models.ForeignKey('category', on_delete=models.CASCADE, related_name='item_category')