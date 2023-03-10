from django.db import models

class PackList(models.Model):

    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='item_packlist')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_item')