import datetime
import logging

from django.dispatch import receiver
from django.db.models.signals import post_save

from django.db import models

logger = logging.getLogger(__name__)


class Consignment(models.Model):
    consignor = models.ForeignKey('Entity', default=0, related_name='consignment_consignor')
    consignee = models.ForeignKey('Entity', default=0, related_name='consignment_consignee')
    originator = models.ForeignKey('Entity', default=0, related_name='consignment_originator')
    account = models.ForeignKey('EntityAccount')
    pickup_tenancy = models.CharField("Tenancy", max_length=255, blank=True)
    pickup_street_num = models.CharField("Street #", max_length=255, blank=True)
    pickup_street = models.CharField("Street", max_length=255, blank=True)
    pickup_town = models.CharField("Town", max_length=255, blank=True)
    pickup_postcode = models.CharField("Postcode", max_length=255, blank=True)
    pickup_state = models.CharField("State", max_length=255, blank=True)
    pickup_country = models.CharField("Country", max_length=255, blank=True)
    delivery_tenancy = models.CharField("Tenancy", max_length=255, blank=True)
    delivery_street_num = models.CharField("Street #", max_length=255, blank=True)
    delivery_street = models.CharField("Street", max_length=255, blank=True)
    delivery_town = models.CharField("Town", max_length=255, blank=True)
    delivery_postcode = models.CharField("Postcode", max_length=255, blank=True)
    delivery_state = models.CharField("State", max_length=255, blank=True)
    delivery_country = models.CharField("Country", max_length=255, blank=True)
    mode = models.CharField('Mode', max_length=64, blank=False)
    status = models.CharField('Status', max_length=64, blank=False)
    pickupDate = models.DateTimeField('Pickup Date', auto_now=True, auto_now_add=True, default=datetime.datetime.now())
    eta_date = models.DateTimeField('ETA', auto_now=True, auto_now_add=True, default=datetime.datetime.now())
    notes = models.CharField('Notes', max_length=512, blank=True)
    customer_reference = models.CharField('Customer Reference', max_length=255, blank=True)

    class Meta:
        ordering = ['-id']


class ConsignmentItem(models.Model):
    consignment = models.ForeignKey('Consignment', default=0, related_name='items')
    description = models.CharField('Description', max_length=255, blank=False)
    width = models.CharField('Width', max_length=16, blank=False)
    length = models.CharField('Length', max_length=16, blank=False)
    height = models.CharField('Height', max_length=16, blank=False)
    dead_weight = models.CharField('Dead Weight', max_length=16, blank=False)
    temp = models.CharField('Temp', max_length=16, blank=False)


class ConsignmentCharge(models.Model):
    consignment = models.ForeignKey('Consignment', default=0, related_name='charges')
    description = models.CharField('Description', max_length=255, blank=False)
    quantity = models.CharField('Quantity', max_length=10, blank=False)
    cost = models.CharField('Cost', max_length=10, blank=False)


class ConsignmentSupply(models.Model):
    consignment = models.ForeignKey('Consignment', related_name='supplies')
    supply = models.ForeignKey('Supply')
    amount = models.CharField('Amount', max_length=10, blank=False)


class Entity(models.Model):
    name = models.CharField("Entity Name", max_length=255, blank=False)
    type = models.CharField("Type", max_length=255, blank=False)
    tenancy = models.CharField("Tenancy", max_length=255, blank=True)
    street_num = models.CharField("Street #", max_length=255, blank=True)
    street = models.CharField("Street", max_length=255, blank=True)
    town = models.CharField("Town", max_length=255, blank=True)
    postcode = models.CharField("Postcode", max_length=255, blank=True)
    state = models.CharField("State", max_length=255, blank=True)
    country = models.CharField("Country", max_length=255, blank=True)
    email = models.EmailField("Email", max_length=64, blank=True)


class EntityAccount(models.Model):
    description = models.CharField("Description", max_length=255, blank=False)
    entity = models.ForeignKey('Entity', related_name='accounts')


class EntityRelationship(models.Model):
    entity = models.ForeignKey('Entity', default=0, related_name='relationships')
    other = models.ForeignKey('Entity', max_length=255, blank=False, related_name='other_relationships')
    relationship = models.CharField('Relationship', max_length=255, blank=False)


class Supply(models.Model):
    description = models.CharField('Description', max_length=255, blank=False)


class Search(models.Model):
    name = models.CharField('Name', max_length=255, blank=False)


class SearchField(models.Model):
    search = models.ForeignKey('Search', related_name='fields')
    name = models.CharField('Field', max_length=255, blank=False)
    title = models.CharField('Title', max_length=255, blank=False)
    selected = models.BooleanField('Selected', default=True)


class SearchCriterion(models.Model):
    search = models.ForeignKey('Search', related_name='criteria')
    criterion = models.CharField('Criteria', max_length=255, blank=False)
    criterion_value = models.CharField('Value', max_length=255, blank=False)


class EntityType:
    def __init__(self, description):
        self.description = description
