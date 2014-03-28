# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import textwrap

from django.core.management.base import BaseCommand
from optparse import make_option

from ralph_assets.others import get_assets_rows, get_licences_rows


class Command(BaseCommand):
    """Export relations report included relations between asset, user and
    licences."""
    help = textwrap.dedent(__doc__).strip()
    option_list = BaseCommand.option_list + (
        make_option(
            '--assets',
            action='store_true',
            dest='only_assets',
            default=False,
            help="Run command to get only Assets report without relations",
        ),
        make_option(
            '--licences',
            action='store_true',
            dest='only_licences',
            default=False,
            help="Run command to get Licences relations with assets and users",
        ),
        make_option(
            '--filter',
            type="choice",
            dest='filter_type',
            choices=["all", "dc", "back_office"],
            default="all",
            help="Filter items, all, dc, back_office",
        ),
    )

    def handle(self, *args, **options):
        only_licences = options['only_licences']
        only_assets = options['only_assets']
        filter_type = options['filter_type']
        if not any((only_licences, only_assets)):
            self.stdout.write(
                'Arguments required, type --help for more informations\n',
            )
        if only_assets and not only_licences:
            for row in get_assets_rows(filter_type):
                self.stdout.write(row.encode('ascii', 'ignore'))
        elif only_licences and not only_assets:
            for row in get_licences_rows(filter_type):
                self.stdout.write(row.encode('ascii', 'ignore'))
