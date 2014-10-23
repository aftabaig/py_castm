# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SearchCriteria'
        db.delete_table(u'api_searchcriteria')

        # Adding model 'SearchCriterion'
        db.create_table(u'api_searchcriterion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('search', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Search'])),
            ('criteria', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'api', ['SearchCriterion'])

        # Adding field 'SearchField.selected'
        db.add_column(u'api_searchfield', 'selected',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'SearchCriteria'
        db.create_table(u'api_searchcriteria', (
            ('search', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.Search'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('criteria', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'api', ['SearchCriteria'])

        # Deleting model 'SearchCriterion'
        db.delete_table(u'api_searchcriterion')

        # Deleting field 'SearchField.selected'
        db.delete_column(u'api_searchfield', 'selected')


    models = {
        u'api.consignment': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Consignment'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.EntityAccount']"}),
            'consignee': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'consignment_consignee'", 'to': u"orm['api.Entity']"}),
            'consignor': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'consignment_consignor'", 'to': u"orm['api.Entity']"}),
            'customer_reference': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'deliveryAddress': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'eta_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 19, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'originator': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'consignment_originator'", 'to': u"orm['api.Entity']"}),
            'pickupAddress': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'pickupDate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 19, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.Search']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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