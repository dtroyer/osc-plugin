================
python-oscplugin
================

OpenStackClient reference plugin module

The OSC plugin system is designed so that the plugin need only be
properly installed for OSC to find and use it.  It utilizes the
``setuptools`` entry points mechanism to advertise to OSC the
plugin module and supported commands.

**oscplugin** is a sample OpenStackClient (OSC) plugin implementation that
demonstrates how to add commands via OSC's extension mechanism.  It adds
two commands (``plugin list`` and ``plugin show``) to demonstrate the simple
case of new commands that do not require authentication.

Discovery
=========

OSC discovers extensions by enumerating the entry points found under
``openstack.cli.extension`` and initializing the given client module.

::

    [entry_points]
    openstack.cli.extension =
        oscplugin = oscplugin.client

The client module must implement the following interface functions:

* ``API_NAME`` - A string containing the plugin API name; this is
  the name of the entry point declaring the plugin client module
  (``oscplugin = ...`` in the example above) and the group name for
  the plugin commands (``openstack.oscplugin.v1 =`` in the example below)
* ``API_VERSION_OPTION`` (optional) - If set, the name of the API
  version attribute; this must be a valid Python identifier and
  match the destination set in ``build_option_parser()``.
* ``API_VERSIONS`` - A dict mapping a version string to the client class
* ``build_option_parser(parser)`` - Hook to add global options to the parser
* ``make_client(instance)`` - Hook to create the client object

OSC enumerates the loaded plugins and loads commands from the entry points
defined for the API version:

::

    openstack.oscplugin.v1 =
        plugin_list = oscplugin.v1.plugin:ListPlugin
        plugin_show = oscplugin.v1.plugin:ShowPlugin

Note that OSC defines the group name as ``openstack.<api-name>.v<version>``
so the version should not contain the leading 'v' character.

This second step is identical to that performed for all but the Identity
client in OSC itself.  Identity is special due to the authentication
requirements.  This limits the ability to add additional auth modules to OSC.

Client
======

The current implementation of the ``oscplugin`` Client class is a
simple subclass of ``keystone.HTTPClient``.  This allows tracking of
the changes being made in ``keystoneclient`` to refactor the Session and
authentication classes.
