from django.db import models

# Create your models here.

class MailList(models.Model):
  sender = models.CharField(max_length=200)
  receiver = models.CharField(max_length=200)

  def __str__(self) -> str:
      return self.receiver