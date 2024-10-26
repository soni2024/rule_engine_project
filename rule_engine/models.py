from django.db import models

class Rule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rule_string = models.TextField()
    ast_representation = models.TextField(default="none")
    created_at = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.name
