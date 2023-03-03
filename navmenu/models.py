from django.db import models


class MenuItem(models.Model):
    menu_name = models.CharField(max_length=100, default="main")
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
