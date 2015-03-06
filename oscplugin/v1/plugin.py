#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Plugin action implementation"""

import logging
import six
import sys

from cliff import lister
from cliff import show

from openstackclient.common import clientmanager

from oscplugin import exceptions


class ListPlugin(lister.Lister):
    """List loaded plugins

    Demonstrates a self-contained list command
    """

    auth_required = False
    log = logging.getLogger(__name__ + ".ListPlugin")

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)

        data = []
        for mod in clientmanager.PLUGIN_MODULES:
            versions = []
            if getattr(mod, 'API_VERSIONS', None):
                versions = mod.API_VERSIONS.keys()
            data.append((
                mod.API_NAME,
                versions,
                mod.__name__,
            ))

        columns = ("Name", "Versions", "Module")
        return (columns, data)


class ShowPlugin(show.ShowOne):
    """Show plugin information

    Demonstrates a self-contained show command
    """

    auth_required = False
    log = logging.getLogger(__name__ + '.ShowPlugin')

    def get_parser(self, prog_name):
        parser = super(ShowPlugin, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<plugin-name>',
            help='Plugin to show',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)

        for mod in clientmanager.PLUGIN_MODULES:
            if mod.API_NAME == parsed_args.name:
                data = {
                    'name': mod.API_NAME,
                    'module': mod.__name__,
                }
                versions = []
                if getattr(mod, 'API_VERSIONS', None):
                    versions = mod.API_VERSIONS.keys()
                for ver in versions:
                    data.update({
                        '%s' % ver: mod.API_VERSIONS[ver],
                    })
                return zip(*sorted(six.iteritems(data)))

        sys.stderr.write("Plugin not found: %s" % parsed_args.name)
        return ([], [])


class ShowCatalog(show.ShowOne):
    """Show service catalog entry

    Demonstrates a command using the existing Identity client
    """

    log = logging.getLogger(__name__ + '.ShowCatalog')

    def get_parser(self, prog_name):
        parser = super(ShowCatalog, self).get_parser(prog_name)
        parser.add_argument(
            'service',
            metavar='<service>',
            help='Service to display (type, name or ID)',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)' % parsed_args)

        identity_client = self.app.client_manager.identity

        endpoints = identity_client.service_catalog.get_endpoints(
            service_type=parsed_args.service)
        for (service, service_endpoints) in six.iteritems(endpoints):
            if service_endpoints:
                info = {"type": service}
                info.update(service_endpoints[0])
                return zip(*sorted(six.iteritems(info)))

        msg = ("No service catalog with a type, name or ID of '%s' "
               "exists." % (parsed_args.service))
        raise exceptions.CommandError(msg)
