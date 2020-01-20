#
# Copyright (C) 2020 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

"""This module defines the parts needed for handling Kickstart data in the service."""

from pykickstart.options import KSOptionParser

from pyanaconda.core.kickstart import VERSION, KickstartSpecification
from pyanaconda.core.kickstart.addon import AddonData

import logging

log = logging.getLogger(__name__)


class HelloWorldData(AddonData):
    """The kickstart data for the Hello World addon."""

    def __init__(self):
        super().__init__()
        self.seen = False
        self.lines = []
        self.reverse = False

    def handle_header(self, args, line_number=None):
        """The handle_header method is called to parse additional arguments
        in the %addon section line.

        args is a list of all the arguments following the addon ID. For
        example, for the line:

            %addon org_fedora_hello_world --reverse --arg2="example"

        handle_header will be called with args=['--reverse', '--arg2="example"']

        :param line_number: the current line number in the kickstart file
        :type line_number: int
        :param args: the list of arguments from the %addon line
        :type args: List[Str]
        """
        # Create the argument parser.
        op = KSOptionParser(
            prog="%addon org_fedora_hello_world",
            version=VERSION,
            description="Configure the Hello World Addon."
        )

        op.add_argument(
            "--reverse",
            action="store_true",
            default=False,
            version=VERSION,
            dest="reverse",
            help="Reverse the display of the addon text."
        )

        # Parse the arguments.
        ns = op.parse_args(args=args, lineno=line_number)

        # Store the result of the parsing.
        self.seen = True
        self.reverse = ns.reverse

    def handle_line(self, line, line_number=None):
        """The handle_line method that is called with every line from this
        addon's %addon section of the kickstart file.

        For example, this kickstart...

        %addon org_fedora_hello_world
        Hello world!
        foo bar baz
        %end

        ...will result in two calls to handle_line, once with "Hello world!"
        and another time with "foo bar baz".

        :param line: a single line from the %addon section
        :type line: str
        :param line_number: number of the line
        :type line_number: int
        """
        # simple example, we just append lines to the lines attribute
        self.lines.append(line)

    def __str__(self):
        """What should end up in the resulting kickstart file, i.e. the %addon
        section containing string representation of the stored data.
        """
        if not self.seen:
            return ""

        section = "\n%addon org_fedora_hello_world"

        if self.reverse:
            section += " --reverse"

        section += "\n"

        for line in self.lines:
            section += line

        if not section.endswith("\n"):
            section += "\n"

        section += "%end\n"
        return section


class HelloWorldKickstartSpecification(KickstartSpecification):

    version = VERSION

    addons = {
        "org_fedora_hello_world": HelloWorldData
    }
