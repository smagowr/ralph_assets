# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
from django.test import TestCase

from ralph.discovery.models_device import Device, DeviceType

from ralph_assets.api_pricing import get_assets, get_asset_parts
from ralph_assets.models_assets import PartInfo, AssetModel
from ralph_assets.tests.util import (
    create_asset,
    create_category,
    create_model,
)


class TestModelAsset(TestCase):
    def setUp(self):
        self.asset = create_asset(
            sn='1111-1111-1111-1111',
            invoice_date=datetime.date(2012, 11, 28),
            support_period=1,
            deprecation_rate=100,
        )
        self.asset.device_info.ralph_device_id = 666
        self.asset.device_info.save()
        self.asset2 = create_asset(
            sn='1111-1111-1111-1112',
            invoice_date=datetime.date(2012, 11, 28),
            support_period=120,
            deprecation_rate=50,
        )
        self.asset2.device_info.ralph_device_id = 667
        self.asset2.device_info.save()
        self.asset3 = create_asset(
            sn='1111-1111-1111-1113',
            invoice_date=datetime.date(2012, 11, 28),
            support_period=120,
            deprecation_rate=50,
            force_deprecation=True,
        )
        dev1 = Device.create(
            [('1', 'sda', 0)],
            model_name='xxx',
            model_type=DeviceType.rack_server,
            allow_stub=1,
        )
        dev1.id = 666
        dev1.save()
        dev2 = Device.create(
            [('1', 'dawdwad', 0)],
            model_name='Unknown',
            model_type=DeviceType.unknown,
            allow_stub=1,
        )
        dev2.id = 667
        dev2.save()

    def test_is_discovered(self):
        self.assertEqual(self.asset.is_discovered, True)
        self.assertEqual(self.asset2.is_discovered, False)
        self.assertEqual(self.asset3.is_discovered, False)

    def test_is_deperecation(self):
        date = datetime.date(2014, 03, 29)
        self.assertEqual(self.asset.get_deprecation_months(), 12)
        self.assertEqual(self.asset2.get_deprecation_months(), 24)
        self.assertEqual(self.asset.is_deprecated(date), True)
        self.assertEqual(self.asset2.is_deprecated(date), False)
        self.assertEqual(self.asset3.is_deprecated(date), True)


class TestApiAssets(TestCase):
    def setUp(self):
        self.category = create_category()
        self.category.is_blade = True
        self.category.save()
        self.model = create_model(category=self.category)
        self.model.save()
        self.asset = create_asset(
            sn='1111-1111-1111-1111',
            invoice_date=datetime.date(2012, 11, 28),
            support_period=1,
            slots=12.0,
            price=100,
            deprecation_rate=100,
            model=self.model,
        )

        part_info = PartInfo(device=self.asset)
        part_info.save()
        self.asset2 = create_asset(
            sn='1111-1111-1111-11132',
            invoice_date=datetime.date(2012, 11, 28),
            support_period=1,
            slots=12.0,
            price=100,
            part_info=part_info,
            deprecation_rate=50,
            model=self.model,
        )

    def tests_api_asset(self):
        date = datetime.date(2014, 03, 29)
        for item in get_assets(date):
            self.assertEqual(item['asset_id'], self.asset.id)
            self.assertEqual(
                item['ralph_id'], self.asset.device_info.ralph_device_id,
            )
            self.assertEqual(item['slots'], self.asset.slots)
            self.assertEqual(item['price'], self.asset.price)
            self.assertEqual(
                item['is_deprecated'],
                self.asset.is_deprecated(date)
            )
            self.assertEqual(item['sn'], self.asset.sn)
            self.assertEqual(item['barcode'], self.asset.barcode)
            self.assertEqual(item['venture_id'], self.asset.venture.id)
            self.assertEqual(item['is_blade'], self.category.is_blade)
            self.assertEqual(item['cores_count'], self.asset.cores_count)

    def tests_api_asset_part(self):
        for item in get_asset_parts():
            self.assertEqual(item['price'], 100)
            # self.assertEqual(item['is_deprecated'], False)
            model = AssetModel.objects.get(name="Model1")
            self.assertEqual(item['model'], model.name)
            self.assertEqual(item['asset_id'], self.asset2.id)
            self.assertEqual(item['sn'], self.asset.sn)
            self.assertEqual(item['barcode'], self.asset.barcode)
