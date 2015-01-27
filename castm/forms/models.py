from django.db import models
from organizations.models import Organization


class RatingForm(models.Model):
    organization = models.ForeignKey(Organization, related_name="forms")
    created_at = models.DateTimeField(auto_now_add=True)


class FormField(models.Model):
    type_choices = (
        ('TXT', 'Text'),
        ('MUL', 'Multi-line'),
        ('SCL', 'Scale'),
        ('RAD', 'Radio Button'),
        ('CHK', 'Checkbox'),
        ('DRPD', 'Drop-down'),
    )
    form = models.ForeignKey(RatingForm, related_name="fields")
    type = models.CharField("Field Type", max_length=5, choices=type_choices, blank=False)
    title = models.CharField("Field Title", max_length=1024, blank=False)
    max_value = models.IntegerField("Max Value", blank=True, null=True)
    use_stars = models.NullBooleanField(default=False, blank=True, null=True)

    def plain(self):
        plain_form = PlainFormField(
            form_id=self.form.id,
            form_type=self.type,
            title=self.title,
            max_value=self.max_value,
            use_stars=self.use_stars,
        )
        plain_items = []
        for item in self.items.all():
            plain_items.append(item.plain())
        plain_form.items = plain_items
        return plain_form


class FieldItem(models.Model):
    field = models.ForeignKey(FormField, related_name="items")
    title = models.CharField("Item Title", max_length=256, blank=False)
    value = models.CharField("Item Value", max_length=256, blank=False)

    class Meta:
        ordering = ['id']

    def plain(self):
        return PlainFieldItem(
            title=self.title,
            value=self.value,
        )


class PlainFormField(object):
    def __init__(self, organization_id=None, form_id=None, form_type=None, title=None, max_value=None, use_stars=None, items=None):
        self.organization_id = organization_id
        self.form_id = form_id
        self.form_type = form_type
        self.title = title
        self.max_value = max_value
        self.user_stars = use_stars
        self.items = items


class PlainFieldItem(object):
    def __init__(self, title=None, value=None):
        self.title = title
        self.value = value
