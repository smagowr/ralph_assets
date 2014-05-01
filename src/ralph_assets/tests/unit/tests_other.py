# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
from django.test import TestCase
from django.contrib.auth.models import User

from ralph_assets.models import AssetManufacturer
from ralph_assets.models_assets import AssetType
from ralph_assets.models_sam import (
    AssetOwner,
    Licence,
    LicenceType,
    SoftwareCategory,
)
from ralph_assets.tests.util import (
    create_asset,
    create_category,
    create_model,
)
from ralph_assets.others import get_assets_rows, get_licences_rows


class TestExportRelations(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.local')
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.first_name = 'Elmer'
        self.user.last_name = 'Stevens'
        self.user.save()

        self.owner = User.objects.create_user('owner', 'owner@test.local')
        self.owner.is_staff = False
        self.owner.is_superuser = False
        self.owner.first_name = 'Eric'
        self.owner.last_name = 'Brown'
        self.owner.save()

        self.category = create_category()
        self.model = create_model(category=self.category)
        self.asset = create_asset(
            sn='1111-1111-1111-1111',
            model=self.model,
            user=self.user,
            owner=self.owner,
            barcode='br-666',
            niw='niw=666',
        )

        self.software_category = SoftwareCategory(
            name='soft-cat1', asset_type=AssetType.DC
        )
        self.software_category.save()

        self.manufacturer = AssetManufacturer(name='test_manufacturer')
        self.manufacturer.save()

        self.licence_type = LicenceType(name='test_licence_type')
        self.licence_type.save()

        self.property_of = AssetOwner(name="test_property")
        self.property_of.save()

        self.licence1 = Licence(
            licence_type=self.licence_type,
            software_category=self.software_category,
            manufacturer=self.manufacturer,
            property_of=self.property_of,
            number_bought=10,
            sn="test-sn",
            niw="niw-666",
            invoice_date=datetime.date(2014, 4, 28),
            invoice_no="666-999-666",
            price=1000.0,
            provider="test_provider",
            asset_type=AssetType.DC,
        )
        self.licence1.save()

    def test_assets_rows(self):
        rows = []
        for row in get_assets_rows():
            rows.append(row)
        self.assertEqual(
            rows,
            [
                u'id, niw, barcode, sn, model__category__name, model__manufact'
                'urer__name, model__name, user__username, user__first_name, us'
                'er__last_name, owner__username, owner__first_name, owner__las'
                't_name, status, service_name, property_of,\n',
                u'1, niw=666, br-666, 1111-1111-1111-1111, Subcategory, Manufa'
                'cturer1, Model1, user, Elmer, Stevens, owner, Eric, Brown, 1,'
                ' None, None, \n',
            ]
        )

    def test_licences_rows(self):
        self.licence1.assets.add(self.asset)
        self.licence1.users.add(self.user)
        self.licence1.users.add(self.owner)
        rows = []
        for row in get_licences_rows():
            rows.append(row)

        self.assertEqual(
            rows,
            [
                u'niw, software_category, number_bought, price, invoice_date, '
                'invoice_no, id, barcode, niw, user__username, user__first_nam'
                'e, user__last_name, owner__username, owner__first_name, owner'
                '__last_name, username, first_name, last_name,single_cost, \n',
                u'niw-666, soft-cat1, 10, 1000, 2014-04-28, 666-999-666, , , ,'
                ' , , , , , , , , , \n',
                u'niw-666, soft-cat1, 10, 1000, 2014-04-28, 666-999-666, 1, br'
                '-666, niw=666, user, Elmer, Stevens, owner, Eric, Brown, , , '
                ', 100, \n',
                u'niw-666, soft-cat1, 10, 1000, 2014-04-28, 666-999-666, , , ,'
                ' , , , , , , user, Elmer, Stevens, 100, \n',
                u'niw-666, soft-cat1, 10, 1000, 2014-04-28, 666-999-666, , , ,'
                ' , , , , , , owner, Eric, Brown, 100, \n',
            ]
        )
