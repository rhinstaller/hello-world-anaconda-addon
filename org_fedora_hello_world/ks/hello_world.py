#
# Copyright (C) 2013  Red Hat, Inc.
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
# Red Hat Author(s): Vratislav Podzimek <vpodzime@redhat.com>
#

"""Module with the HelloWorldData class."""

import os.path

from pyanaconda.addons import AddonData
from pyanaconda.core.configuration.anaconda import conf

from pykickstart.options import KSOptionParser
from pykickstart.version import F30

# export HelloWorldData class to prevent Anaconda's collect method from taking
# AddonData class instead of the HelloWorldData class
# :see: pyanaconda.kickstart.AnacondaKSHandler.__init__

__all__ = ["HelloWorldData"]

HELLO_FILE_PATH = "/root/hello_world_addon_output.txt"


class HelloWorldData(AddonData):
    """
    Class parsing and storing data for the Hello world addon.

    :see: pyanaconda.addons.AddonData

    """

    def __init__(self, name):
        """
        :param name: name of the addon
        :type name: str

        """

        AddonData.__init__(self, name)
        self.text = ""
        self.reverse = False

    def __str__(self):
        """
        What should end up in the resulting kickstart file, i.e. the %addon
        section containing string representation of the stored data.

        """

        addon_str = "%%addon %s" % self.name

        if self.reverse:
            addon_str += " --reverse"

        addon_str += "\n%s\n%%end\n" % self.text
        return addon_str

    def handle_header(self, lineno, args):
        """
        The handle_header method is called to parse additional arguments in the
        %addon section line.

        args is a list of all the arguments following the addon ID. For
        example, for the line:

            %addon org_fedora_hello_world --reverse --arg2="example"

        handle_header will be called with args=['--reverse', '--arg2="example"']

        :param lineno: the current line number in the kickstart file
        :type lineno: int
        :param args: the list of arguments from the %addon line
        :type args: list
        """
        op = KSOptionParser(
            prog="addon org_fedora_hello_world", version=F30,
            description="Configure the Hello World Addon.")

        op.add_argument(
            "--reverse", action="store_true", default=False, version=F30,
            dest="reverse", help="Reverse the display of the addon text."
        )

        # Parse the arguments.
        ns = op.parse_args(args=args, lineno=lineno)

        # Store the result of the parsing.
        self.reverse = ns.reverse

    def handle_line(self, line):
        """
        The handle_line method that is called with every line from this addon's
        %addon section of the kickstart file.

        :param line: a single line from the %addon section
        :type line: str

        """

        # simple example, we just append lines to the text attribute
        if self.text is "":
            self.text = line.strip()
        else:
            self.text += " " + line.strip()

    def finalize(self):
        """
        The finalize method that is called when the end of the %addon section
        (i.e. the %end line) is processed. An addon should check if it has all
        required data. If not, it may handle the case quietly or it may raise
        the KickstartValueError exception.

        """

        # no actions needed in this addon
        pass

    def setup(self, storage, ksdata, payload):
        """
        The setup method that should make changes to the runtime environment
        according to the data stored in this object.

        :param storage: object storing storage-related information
                        (disks, partitioning, bootloader, etc.)
        :type storage: blivet.Blivet instance
        :param ksdata: data parsed from the kickstart file and set in the
                       installation process
        :type ksdata: pykickstart.base.BaseHandler instance
        :param payload: object managing packages and environment groups
                        for the installation
        :type payload: any class inherited from the pyanaconda.packaging.Payload
                       class
        """

        # no actions needed in this addon
        pass

    def execute(self, storage, ksdata, users, payload):
        """
        The execute method that should make changes to the installed system. It
        is called only once in the post-install setup phase.

        :see: setup
        :param users: information about created users
        :type users: pyanaconda.users.Users instance

        """

        hello_file_path = os.path.normpath(conf.target.system_root + HELLO_FILE_PATH)
        with open(hello_file_path, "w") as fobj:
            fobj.write("%s\n" % self.text)
