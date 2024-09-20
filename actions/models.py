from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Action(models.Model):
    user = models.ForeignKey('auth.User',related_name='actions',db_index=True,on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    # ContentType This will tell you the model for the relationship
    target_ct = models.ForeignKey(ContentType,blank=True,null=True,related_name='target_obj',on_delete=models.CASCADE)
    # PositiveIntegerField to match Django's automatic primary key fields
    target_id = models.PositiveIntegerField(null=True,blank=True,db_index=True)

    # GenericForeignKey field to the related object based on the combination of the two previous fields
    # The GenericForeignKey field does not appear in the form
    # allows you to select any of the registered models of your Django project
    target = GenericForeignKey('target_ct', 'target_id')
    # Automatically set the current time
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)
