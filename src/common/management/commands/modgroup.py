# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along along
# with this program; if not, write to the
#
#   Free Software Foundation, Inc.
#   51 Franklin Street - Fifth Floor
#   Boston MA  02110-1301
#   USA
#
# Copyright (C) 2013-2014 Luca Filipozzi <lfilipoz@debian.org>
# Copyright (C) 2013 Oliver Berger <obergix@debian.org>
# Copyright (c) 2014 Martin Zobel-Helas <zobel@debian.org>

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from common.models import DebianGroup, DebianRole, DebianUser

import getpass
import ldap
import optparse
import os
import gettext

from _handler import Handler
from _utilities import load_configuration_file

# Set up message catalog access
t = gettext.translation('ud', 'locale', fallback=True)
_ = t.ugettext

class Command(BaseCommand):
    args = '<gid>'
    help = _('Provides an interactive attribute editor for Group entries.')
    option_list = BaseCommand.option_list + (
        optparse.make_option('-D', '--binddn',
            action='store',
            default='',
            help=_('specify bind dn')
        ),
        optparse.make_option('-w', '--passwd',
            action='store',
            default='',
            help=_('specify password')
        ),
        optparse.make_option('--config',
            action='store',
            default='/etc/ud/interactive.yaml',
            help=_('specify configuration file')
        ),
    )

    def handle(self, *args, **options):
        logged_in_uid = ''
        looked_up_gid = ''

        if len(args) == 1:
            looked_up_gid = args[0]
        else:
            raise CommandError(_('must specify at most one gid as argument'))

        try:
            load_configuration_file(options['config'])
        except Exception as err:
            raise CommandError(err)

        if not options['binddn']:
            options['binddn'] = getpass.getuser()
        if options['binddn'].endswith(DebianUser.base_dn):
            settings.DATABASES['ldap']['USER'] = options['binddn']
            logged_in_uid = options['binddn'].split(',')[0].split('=')[0]
        else:
            settings.DATABASES['ldap']['USER'] = 'uid=%s,%s' % (options['binddn'], DebianUser.base_dn)
            logged_in_uid = options['binddn']

        if not options['passwd']:
            try:
                options['passwd'] = getpass.getpass()
            except EOFError:
                self.stdout.write('\n')
                return
        if not options['passwd']:
            raise CommandError(_('must specify password'))
        settings.DATABASES['ldap']['PASSWORD'] = options['passwd']

        try:
            logged_in_user = DebianUser.objects.get(uid=logged_in_uid)
            looked_up_group = DebianGroup.objects.get(gid=looked_up_gid)
            if 'adm' in logged_in_user.supplementaryGid:
                Handler(self.stdout, looked_up_group, logged_in_user).cmdloop()
            else:
                raise CommandError(_('insufficient privileges'))
        except ObjectDoesNotExist:
            raise CommandError(_('group not found'))
        except ldap.INVALID_CREDENTIALS:
            raise CommandError(_('invalid credentials'))
        except Exception as err:
            raise CommandError(err)


# vim: set ts=4 sw=4 et ai si sta:
