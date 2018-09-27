from django.db import models

class Card(models.Model):
    text = models.TextField()
    formatted_text = models.TextField()
    newList = []
    
    def __str(self):
        return self.text
