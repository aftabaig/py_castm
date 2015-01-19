from django.db import models
from organizations.models import Organization


class RatingForm(models.Model):
    organization = models.ForeignKey(Organization, related_name="forms")
    created_at = models.DateTimeField(auto_now_add=True)


class FormField(models.Model):
    type_choices = (
        ('TXT', 'Text'),
        ('MUL', 'Multiline'),
        ('SCL', 'Scale'),
        ('RAD', 'Radio Button'),
        ('CHK', 'Checkbox'),
        ('DRPD', 'Dropdown'),
    )
    form = models.ForeignKey(RatingForm, related_name="fields")
    type = models.CharField("Field Type", max_length=5, choices=type_choices, blank=False)
    title = models.CharField("Field Title", max_length=1024, blank=False)
    max_value = models.IntegerField("Max Value", blank=True, null=True)
    use_stars = models.BooleanField(default=False, blank=True, null=True)


class FieldItem(models.Model):
    field = models.ForeignKey(FormField, related_name="items")
    title = models.CharField("Item Title", max_length=256, blank=False)
    value = models.CharField("Item Value", max_length=256, blank=False)
