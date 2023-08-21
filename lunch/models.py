from django.db import models
from general.models import BaseModel


class Dish(BaseModel):
    """Model to create Dish"""
    name = models.TextField()

    def __str__(self):
        """return first_name of officer"""
        return self.name
    
    class Meta:
        verbose_name_plural = "Dishes"

class LunchMenu(BaseModel):
    """Model to create LunchMenu"""
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    date = models.DateField()
    
    def __str__(self):
        """return dish name"""
        return f"{self.dish.name}({self.date})"
