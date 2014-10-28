# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ConsignmentSupply'
        db.delete_table(u'api_consignmentsupply')

        # Adding M2M table for field consignments on 'Supply'
        m2m_table_name = db.shorten_name(u'api_supply_consignments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('supply', models.ForeignKey(orm[u'api.supply'], null=False)),
            ('consignment', models.ForeignKey(orm[u'api.consignment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['supply_id', 'consignment_id'])


    def backwards(self, orm):
        # Adding model 'ConsignmentSupply'
        db.create_table(u'api_consignmentsupply', (
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('consignment', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='supplies', to=orm['api.Consignment'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supply', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='', to=orm['api.Consignment'])),
        ))
        db.send_create_signal(u'api', ['ConsignmentSupply'])

        # Removing M2M table for field consignments on 'Supply'
        db.delete_table(db.shorten_name(u'api_supply_consignments'))


    models = {
        u'api.consignment': {
            'Meta': {'object_name': 'Consignment'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'consignee': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'consignment_consignee'", 'to': u"orm['api.Entity']"}),
            'consignor': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'consignment_consignor'", 'to': u"orm['api.Entity']"}),
            'deliveryAddress': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'pickupAddress': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'pickupDate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 18, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
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
        u'api.supply': {
            'Meta': {'object_name': 'Supply'},
            'consignments': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['api.Consignment']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['api']