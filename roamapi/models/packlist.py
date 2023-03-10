from django.db import models

class PackList(models.Model):

    item = models.ForeignKey('PackListItem', on_delete=models.CASCADE, related_name='item_packlist')
    category = models.ForeignKey('PackListCategory', on_delete=models.CASCADE, related_name='category_item')