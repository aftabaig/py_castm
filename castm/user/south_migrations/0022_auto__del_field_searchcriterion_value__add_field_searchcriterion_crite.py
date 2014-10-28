# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SearchCriterion.value'
        db.delete_column(u'api_searchcriterion', 'value')

        # Adding field 'SearchCriterion.criteria_value'
        db.add_column(u'api_searchcriterion', 'criteria_value',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'SearchCriterion.value'
        db.add_column(u'api_searchcriterion', 'value',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'SearchCriterion.criteria_value'
        db.delete_column(u'api_searchcriterion', 'criteria_value')


    models = {
        u'api.consignment': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Consignment'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.EntityAccount']"}),
            'consignee': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'consignment_consignee'", 'to': u"orm['api.Entity']"}),
            'consignor': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'consignment_consignor'", 'to': u"orm['api.Entity']"}),
            'customer_reference': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'delivery_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'delivery_postcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'delivery_state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'delivery_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'delivery_street_num': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'delivery_tenancy': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'delivery_town': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'eta_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 22, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'originator': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'consignment_originator'", 'to': u"orm['api.Entity']"}),
            'pickupDate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 22, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'pickup_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pickup_postcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pickup_state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pickup_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pickup_street_num': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pickup_tenancy': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pickup_town': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'api.consignmentcharge': {
            'Meta': {'object_name': 'ConsignmentCharge'},
            'consignment': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'charges'", 'to': u"orm['api.Consignment']"}),
            'cost': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'api.consignmentitem': {
            'Meta': {'object_name': 'ConsignmentItem'},
            'consignment': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'items'", 'to': u"orm['api.Consignment']"}),
            'dead_weight': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'temp': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'api.consignmentsupply': {
            'Meta': {'object_name': 'ConsignmentSupply'},
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'consignment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supplies'", 'to': u"orm['api.Consignment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'supply': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Supply']"})
        },
        u'api.entity': {
            'Meta': {'object_name': 'Entity'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_num': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tenancy': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'api.entityaccount': {
            'Meta': {'object_name': 'EntityAccount'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts'", 'to': u"orm['api.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'api.entityrelationship': {
            'Meta': {'object_name': 'EntityRelationship'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'relationships'", 'to': u"orm['api.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'other_relationships'", 'max_length': '255', 'to': u"orm['api.Entity']"}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'api.search': {
            'Meta': {'object_name': 'Search'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'api.searchcriterion': {
            'Meta': {'object_name': 'SearchCriterion'},
            'criteria': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'criteria_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Search']"})
        },
        u'api.searchfield': {
            'Meta': {'object_name': 'SearchField'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Search']"}),
            'selected': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'api.supply': {
            'Meta': {'object_name': 'Supply'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['api']