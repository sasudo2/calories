
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=1, default='M')
    set = models.BooleanField(default=False)


class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    t_quantity = models.FloatField(default=0)
    t_calories = models.FloatField(default=0)
    t_protein = models.FloatField(default=0)
    t_carbs = models.FloatField(default=0)
    t_cholesterol = models.FloatField(default=0)
    t_fat_saturated = models.FloatField(default=0)
    t_fat = models.FloatField(default=0)
    t_fiber = models.FloatField(default=0)
    t_sugar = models.FloatField(default=0)
    t_sodium = models.FloatField(default=0)
    t_potassium = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True)
    def to_dict(self):
        return {
            "t_quantity": self.t_quantity,
            "t_calories": self.t_calories,
            "t_protein": self.t_protein,
            "t_carbs": self.t_carbs,
            "t_cholesterol": self.t_cholesterol,
            "t_fat_saturated": self.t_fat_saturated,
            "t_fat": self.t_fat,
            "t_fiber": self.t_fiber,
            "t_sugar": self.t_sugar,
            "t_sodium": self.t_sodium,
            "t_potassium": self.t_potassium
        }
