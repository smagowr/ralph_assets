# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AssetOwner'
        db.create_table('ralph_assets_assetowner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=75, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('cache_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('ralph_assets', ['AssetOwner'])

        # Adding model 'Licence'
        db.create_table('ralph_assets_licence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('cache_version', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ralph_assets.AssetManufacturer'], null=True, on_delete=models.PROTECT, blank=True)),
            ('licence_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ralph_assets.LicenceType'], on_delete=models.PROTECT)),
            ('property_of', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ralph_assets.AssetOwner'], null=True, on_delete=models.PROTECT)),
            ('software_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ralph_assets.SoftwareCategory'], on_delete=models.PROTECT)),
            ('number_bought', self.gf('django.db.models.fields.IntegerField')()),
            ('sn', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True, null=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name=u'children', null=True, to=orm['ralph_assets.Licence'])),
            ('niw', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('bought_date', self.gf('django.db.models.fields.DateField')()),
            ('valid_thru', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('order_no', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2)),
            ('accounting_id', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('asset_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('used', self.gf('django.db.models.fields.IntegerField')()),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('ralph_assets', ['Licence'])

        # Adding model 'SoftwareCategory'
        db.create_table('ralph_assets_softwarecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=75, db_index=True)),
            ('asset_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('ralph_assets', ['SoftwareCategory'])

        # Adding model 'LicenceType'
        db.create_table('ralph_assets_licencetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=75, db_index=True)),
        ))
        db.send_create_signal('ralph_assets', ['LicenceType'])

        # Adding field 'Asset.task_url'
        db.add_column('ralph_assets_asset', 'task_url',
                      self.gf('django.db.models.fields.URLField')(max_length=2048, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Asset.property_of'
        db.add_column('ralph_assets_asset', 'property_of',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ralph_assets.AssetOwner'], null=True, on_delete=models.PROTECT, blank=True),
                      keep_default=False)

        # Adding field 'Asset.owner'
        db.add_column('ralph_assets_asset', 'owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'owner', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Asset.user'
        db.add_column('ralph_assets_asset', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'user', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'AssetModel.type'
        db.add_column('ralph_assets_assetmodel', 'type',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'AssetOwner'
        db.delete_table('ralph_assets_assetowner')

        # Deleting model 'Licence'
        db.delete_table('ralph_assets_licence')

        # Deleting model 'SoftwareCategory'
        db.delete_table('ralph_assets_softwarecategory')

        # Deleting model 'LicenceType'
        db.delete_table('ralph_assets_licencetype')

        # Deleting field 'Asset.task_url'
        db.delete_column('ralph_assets_asset', 'task_url')

        # Deleting field 'Asset.property_of'
        db.delete_column('ralph_assets_asset', 'property_of_id')

        # Deleting field 'Asset.owner'
        db.delete_column('ralph_assets_asset', 'owner_id')

        # Deleting field 'Asset.user'
        db.delete_column('ralph_assets_asset', 'user_id')

        # Deleting field 'AssetModel.type'
        db.delete_column('ralph_assets_assetmodel', 'type')


    models = {
        'account.profile': {
            'Meta': {'object_name': 'Profile'},
            'activation_token': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '40', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'country': ('django.db.models.fields.PositiveIntegerField', [], {'default': '153'}),
            'gender': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'home_page': (u'dj.choices.fields.ChoiceField', [], {'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'blank': 'False', u'default': '1', 'null': 'False', '_in_south': 'True', 'db_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_active': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'nick': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '30', 'blank': 'True'}),
            'time_zone': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ralph_assets.asset': {
            'Meta': {'object_name': 'Asset'},
            'barcode': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetCategory']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'delivery_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deprecation_rate': ('django.db.models.fields.DecimalField', [], {'default': '25', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'device_info': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ralph_assets.DeviceInfo']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'force_deprecation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetModel']", 'on_delete': 'models.PROTECT'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'niw': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'office_info': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ralph_assets.OfficeInfo']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'order_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'owner'", 'null': 'True', 'to': "orm['auth.User']"}),
            'part_info': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ralph_assets.PartInfo']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'production_use_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'production_year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'property_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetOwner']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'provider_order_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'request_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slots': ('django.db.models.fields.FloatField', [], {'default': '0', 'max_length': '64'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'support_period': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'support_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'support_type': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'support_void_reporting': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'task_url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'user'", 'null': 'True', 'to': "orm['auth.User']"}),
            'warehouse': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.Warehouse']", 'on_delete': 'models.PROTECT'})
        },
        'ralph_assets.assetcategory': {
            'Meta': {'object_name': 'AssetCategory'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_blade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': "orm['ralph_assets.AssetCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'ralph_assets.assethistorychange': {
            'Meta': {'object_name': 'AssetHistoryChange'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ralph_assets.Asset']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'device_info': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ralph_assets.DeviceInfo']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_value': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'office_info': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ralph_assets.OfficeInfo']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'old_value': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'part_info': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['ralph_assets.PartInfo']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'ralph_assets.assetmanufacturer': {
            'Meta': {'object_name': 'AssetManufacturer'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.assetmodel': {
            'Meta': {'object_name': 'AssetModel'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetCategory']", 'null': 'True', 'blank': 'True'}),
            'cores_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'height_of_device': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetManufacturer']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'}),
            'power_consumption': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        'ralph_assets.assetowner': {
            'Meta': {'object_name': 'AssetOwner'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.deviceinfo': {
            'Meta': {'object_name': 'DeviceInfo'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'rack': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'ralph_device_id': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'u_height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'u_level': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'ralph_assets.licence': {
            'Meta': {'object_name': 'Licence'},
            'accounting_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'asset_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'bought_date': ('django.db.models.fields.DateField', [], {}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'licence_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.LicenceType']", 'on_delete': 'models.PROTECT'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetManufacturer']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'niw': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'number_bought': ('django.db.models.fields.IntegerField', [], {}),
            'order_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': "orm['ralph_assets.Licence']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'property_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.AssetOwner']", 'null': 'True', 'on_delete': 'models.PROTECT'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'software_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ralph_assets.SoftwareCategory']", 'on_delete': 'models.PROTECT'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'used': ('django.db.models.fields.IntegerField', [], {}),
            'valid_thru': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'ralph_assets.licencetype': {
            'Meta': {'object_name': 'LicenceType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.officeinfo': {
            'Meta': {'object_name': 'OfficeInfo'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_of_last_inventory': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_logged_user': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'license_key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'license_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'ralph_assets.partinfo': {
            'Meta': {'object_name': 'PartInfo'},
            'barcode_salvaged': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'device'", 'null': 'True', 'to': "orm['ralph_assets.Asset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'source_device': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'source_device'", 'null': 'True', 'to': "orm['ralph_assets.Asset']"})
        },
        'ralph_assets.softwarecategory': {
            'Meta': {'object_name': 'SoftwareCategory'},
            'asset_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        },
        'ralph_assets.warehouse': {
            'Meta': {'object_name': 'Warehouse'},
            'cache_version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75', 'db_index': 'True'})
        }
    }

    complete_apps = ['ralph_assets']
