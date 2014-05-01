# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.template.defaultfilters import slugify


class Migration(SchemaMigration):

    def update_slug_and_child(self, assetcategoryid):
        assetcategoryid = int(assetcategoryid[0])
        for id, type, parent_id, parent_new_id, name in db.execute(
            'SELECT id, type, parent_id, parent_new_id, name FROM ralph_assets_assetcategory WHERE id = %s',
            [assetcategoryid]):
            par_new_id = str(parent_new_id)
            if parent_new_id is None:
                par_new_id = ''
            s = str(type) + " " + \
                par_new_id + " " + name
            slug = slugify(s)
            db.execute("UPDATE ralph_assets_asset SET category_new_id = %s "
                       "WHERE category_id = %s",
                        [slug, id])
            db.execute("UPDATE ralph_assets_assetmodel SET category_new_id = %s "
                       "WHERE category_id = %s",
                        [slug, id])
            db.execute("UPDATE ralph_assets_assetcategory SET parent_new_id = %s "
                       "WHERE parent_id = %s",
                        [slug, id])
            db.execute("UPDATE ralph_assets_assetcategory SET slug = %s "
                       "WHERE id = %s",
                        [slug, id])
            for id in db.execute(
                'SELECT id FROM ralph_assets_assetcategory WHERE parent_id = %s',
                [id]):
                self.update_slug_and_child(id)

    def forwards(self, orm):
        # Changing field 'AssetCategory.id' (serial)
        # to 'AssetCategory.slug' (slugfield)
        db.add_column('ralph_assets_assetcategory', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='slug',
                      unique=False, max_length=100),
                      keep_default=False)
        db.add_column('ralph_assets_asset', 'category_new_id',
                      self.gf('django.db.models.fields.SlugField')(null=True,
                      unique=False, max_length=100, db_index=False))
        db.add_column('ralph_assets_assetcategory', 'parent_new_id',
                      self.gf('django.db.models.fields.SlugField')(null=True,
                      unique=False, max_length=100, db_index=False))
        db.add_column('ralph_assets_assetmodel', 'category_new_id',
                      self.gf('django.db.models.fields.SlugField')(null=True,
                      unique=False, max_length=100, db_index=False))

        db.start_transaction()

        for id in db.execute(
            'SELECT id FROM ralph_assets_assetcategory WHERE parent_id IS NULL'):
            self.update_slug_and_child(id)

        db.commit_transaction()

        db.create_unique(u'ralph_assets_assetcategory', ['slug'])
        db.delete_foreign_key("ralph_assets_asset", "category_id")
        db.delete_foreign_key("ralph_assets_assetmodel", "category_id")
        db.delete_foreign_key("ralph_assets_assetcategory", "parent_id")
        db.delete_column('ralph_assets_assetcategory', 'parent_id')
        db.delete_column('ralph_assets_assetcategory', 'id')
        db.create_primary_key("ralph_assets_assetcategory", ["slug"])
        db.send_create_signal('ralph_assets', ['ralph_assets_assetcategory'])
        db.rename_column('ralph_assets_assetcategory', 'parent_new_id', 'parent_id')
        db.delete_column('ralph_assets_asset', 'category_id')
        db.rename_column('ralph_assets_asset', 'category_new_id', 'category_id')
        db.delete_column('ralph_assets_assetmodel', 'category_id')
        db.rename_column('ralph_assets_assetmodel', 'category_new_id', 'category_id')
        db.create_index('ralph_assets_assetcategory', ['parent_id'], unique=False)
        db.create_index('ralph_assets_asset', ['category_id'], unique=False)
        db.create_index('ralph_assets_assetmodel', ['category_id'], unique=False)
        sql = db.foreign_key_sql('ralph_assets_asset',
            'category_id', 'ralph_assets_assetcategory', 'slug')
        db.execute(sql)
        sql = db.foreign_key_sql('ralph_assets_assetmodel',
            'category_id', 'ralph_assets_assetcategory', 'slug')
        db.execute(sql)
        sql = db.foreign_key_sql('ralph_assets_assetcategory',
            'parent_id', 'ralph_assets_assetcategory', 'slug')
        db.execute(sql)
        try:
            db.delete_unique('ralph_assets_assetcategory', ['name'])
        except ValueError:
            pass

    def backwards(self, orm):
        db.delete_primary_key("ralph_assets_assetcategory")
        db.add_column('ralph_assets_assetcategory', 'parent_new_id',
                      self.gf('django.db.models.fields.IntegerField')(blank=True,
                      null=True, db_index=False))
        db.add_column('ralph_assets_assetcategory', 'id',
                      self.gf('django.db.models.fields.AutoField')(blank=True,
                      null=False, db_index=False, primary_key=True, max_length=10))
        db.add_column('ralph_assets_asset', 'category_new_id',
                      self.gf('django.db.models.fields.IntegerField')(blank=True,
                      null=True, db_index=False))
        db.add_column('ralph_assets_assetmodel', 'category_new_id',
                      self.gf('django.db.models.fields.IntegerField')(blank=True,
                      null=True, db_index=False))
        db.start_transaction()
        for i, slug in enumerate(
            db.execute('SELECT slug FROM ralph_assets_assetcategory')):
            slug = slug[0]
            db.execute("UPDATE ralph_assets_assetcategory SET id = %s "
                       "WHERE slug = %s",
                        [i+1, slug])
            db.execute("UPDATE ralph_assets_assetcategory SET parent_new_id = %s "
                       "WHERE parent_id = %s",
                        [i+1, slug])
            db.execute("UPDATE ralph_assets_asset SET category_new_id = %s "
                       "WHERE category_id = %s",
                        [i+1, slug])
            db.execute("UPDATE ralph_assets_assetmodel SET category_new_id = %s "
                       "WHERE category_id = %s",
                        [i+1, slug])
        db.commit_transaction()
        db.delete_column('ralph_assets_assetcategory', 'slug')
        db.delete_column('ralph_assets_assetcategory', 'parent_id')
        db.rename_column('ralph_assets_assetcategory', 'parent_new_id', 'parent_id')
        db.delete_column('ralph_assets_asset', 'category_id')
        db.rename_column('ralph_assets_asset', 'category_new_id', 'category_id')
        db.delete_column('ralph_assets_assetmodel', 'category_id')
        db.rename_column('ralph_assets_assetmodel', 'category_new_id', 'category_id')
        sql = db.foreign_key_sql('ralph_assets_asset',
            'category_id', 'ralph_assets_assetcategory', 'id')
        db.execute(sql)
        sql = db.foreign_key_sql('ralph_assets_assetmodel',
            'category_id', 'ralph_assets_assetcategory', 'id')
        db.execute(sql)
        sql = db.foreign_key_sql('ralph_assets_assetcategory',
            'parent_id', 'ralph_assets_assetcategory', 'id')
        db.execute(sql)
        db.create_index('ralph_assets_assetcategory', ['parent_id'], unique=False)
        db.create_index('ralph_assets_asset', ['category_id'], unique=False)
        db.create_index('ralph_assets_assetmodel', ['category_id'], unique=False)

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
            'is_blade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['account.Profile']", 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'False', 'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': "orm['ralph_assets.AssetCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True', 'primary_key': 'True'})
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
