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

import sys

from oscplugin.tests import base
from oscplugin.tests import fakes
from oscplugin.v1 import plugin

# Load the plugin init module for the plugin list and show commands
import oscplugin.plugin
plugin_name = 'oscplugin'
plugin_client = 'oscplugin.plugin'


class FakePluginV1Client(object):
    def __init__(self, **kwargs):
        #self.servers = mock.Mock()
        #self.servers.resource_class = fakes.FakeResource(None, {})
        self.auth_token = kwargs['token']
        self.management_url = kwargs['endpoint']


class TestPluginV1(base.TestCommand):
    def setUp(self):
        super(TestPluginV1, self).setUp()

        self.app.client_manager.oscplugin = FakePluginV1Client(
            endpoint=fakes.AUTH_URL,
            token=fakes.AUTH_TOKEN,
        )

        # Get a shortcut to the Service Catalog Mock
        #self.catalog_mock = self.app.client_manager.identity.service_catalog
        #self.catalog_mock.reset_mock()


class TestPluginList(TestPluginV1):

    def setUp(self):
        super(TestPluginList, self).setUp()

        self.app.ext_modules = [
            sys.modules[plugin_client],
        ]

        # Get the command object to test
        self.cmd = plugin.ListPlugin(self.app, None)

    def test_plugin_list(self):
        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        collist = ('Name', 'Versions', 'Module')
        self.assertEqual(columns, collist)
        datalist = ((
            plugin_name,
            oscplugin.plugin.API_VERSIONS.keys(),
            plugin_client,
        ), )
        self.assertEqual(tuple(data), datalist)


class TestPluginShow(TestPluginV1):

    def setUp(self):
        super(TestPluginShow, self).setUp()

        self.app.ext_modules = [
            sys.modules[plugin_client],
        ]

        # Get the command object to test
        self.cmd = plugin.ShowPlugin(self.app, None)

    def test_plugin_show(self):
        arglist = [
            plugin_name,
        ]
        verifylist = [
            ('name', plugin_name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # DisplayCommandBase.take_action() returns two tuples
        columns, data = self.cmd.take_action(parsed_args)

        collist = ('1', 'module', 'name')
        self.assertEqual(columns, collist)
        datalist = (
            oscplugin.plugin.API_VERSIONS['1'],
            plugin_client,
            plugin_name,
        )
        self.assertEqual(data, datalist)
