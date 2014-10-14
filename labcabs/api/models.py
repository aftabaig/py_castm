import datetime

from django.db import models


class Consignment(models.Model):
    consignor = models.ForeignKey('Entity', default=0, related_name='consignment_consignor')
    consignee = models.ForeignKey('Entity', default=0, related_name='consignment_consignee')
    account = models.CharField('Account', max_length=255, blank=False)
    mode = models.CharField('Mode', max_length=64, blank=False)
    status = models.CharField('Status', max_length=64, blank=False)
    pickupDate = models.DateTimeField('Pickup Date', auto_now=True, auto_now_add=True, default=datetime.datetime.now())
    notes = models.CharField('Notes', max_length=512, blank=True)


class ConsignmentItem(models.Model):
    consignment = models.ForeignKey('Consignment', default=0, related_name='items')
    description = models.CharField('Description', max_length=255, blank=False)
    width = models.CharField('Width', max_length=16, blank=False)
    length = models.CharField('Length', max_length=16, blank=False)
    height = models.CharField('Height', max_length=16, blank=False)
    weight = models.CharField('Weight', max_length=16, blank=False)
    temp = models.CharField('Temp', max_length=16, blank=False)


class ConsignmentCharge(models.Model):
    consignment = models.ForeignKey('Consignment', default=0, related_name='charges')
    description = models.CharField('Description', max_length=255, blank=False)
    quantity = models.CharField('Quantity', max_length=10, blank=False)
    cost = models.CharField('Cost', max_length=10, blank=False)


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


class EntityRelationship(models.Model):
    entity = models.ForeignKey('Entity', default=0, related_name='entity_relationships')
    other = models.ForeignKey('Entity', max_length=255, blank=False, related_name='other_relationships')
    relationship = models.CharField('Relationship', max_length=255, blank=False)


