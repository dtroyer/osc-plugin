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

"""Plugin command extension"""

import logging

from cliff import hooks


class FlavorHook(hooks.CommandHook):
    def __init__(self, command):
        super(FlavorHook, self).__init__(command)
        print("FlavorHook.__init__()")

    def get_epilog(self):
        return 'FlavorHook epilog text'

    def get_parser(self, parser):
        parser.add_argument(
            "--ram",
            type=int,
            metavar="<size-mb>",
            help="List flavors with minimum memory size (in MB)",
        )
        parser.add_argument(
            "--disk",
            type=int,
            metavar="<size-gb>",
            help="List flavors with minimum disk size (in GB)",
        )
        parser.add_argument(
            "--vcpus",
            type=int,
            metavar="<vcpus>",
            help="List flavors with minimum number of vcpus",
        )
        return parser

    def before(self, parsed_args):

        return parsed_args

    def after(self, parsed_args, return_code):
        ret_data = []
        data = return_code[1]

        # Convert the flavor args to a flavor
        flair = {}
        for i in ['ram', 'disk', 'vcpus']:
            if i in parsed_args and getattr(parsed_args, i, None) is not None:
                flair[i] = getattr(parsed_args, i, None)

        if len(flair) > 0:
            for f in data:
                result = True
                # TODO(dtroyer): Do the following based on the columns tuple
                if 'ram' in flair:
                    result = result and (flair['ram'] <= f[2])
                if 'disk' in flair:
                    result = result and (flair['disk'] <= f[3])
                if 'vcpus' in flair:
                    result = result and (flair['vcpus'] <= f[5])

                if result:
                    print("FlavorHook.after(): %s" % f[0])
                    ret_data.append(f)

        print("ret_data: %s" % ret_data)
        return (return_code[0], ret_data)

