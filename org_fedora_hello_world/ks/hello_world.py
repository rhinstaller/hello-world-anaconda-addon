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
from pyanaconda.constants import ROOT_PATH

# export HelloWorldData class to prevent Anaconda's collect method from taking
# AddonData class instead of the HelloWorldData class
# (@see: pyanaconda.kickstart.AnacondaKSHandler.__init__)
__all__ = ["HelloWorldData"]

HELLO_FILE_PATH = "/root/hello_world_addon_output.txt"

class HelloWorldData(AddonData):
    """
    Class parsing and storing data for the Hello world addon.

    @see: pyanaconda.addons.AddonData

    """

    def __init__(self, name):
        """
        @param name: name of the addon
        @type name: str

        """

        AddonData.__init__(self, name)
        self.text = ""

    def __str__(self):
        """
        What should end up between %addon and %end lines in the resulting
        kickstart file, i.e. string representation of the stored data.

        """

        return self.text

    def handle_line(self, line):
        """
        The handle_line method that is called with every line from this addon's
        %addon section of the kickstart file.

        @param line: a single line from the %addon section
        @type line: str

        """

        # simple example, we just append lines to the text attribute
        self.text += " " + line.strip()

    def setup(self, storage, ksdata, instclass):
        """
        The setup method that should make changes to the runtime environment
        according to the data stored in this object.

        @param storage: object storing storage-related information
                        (disks, partitioning, bootloader, etc.)
        @type storage: blivet.Blivet instance
        @param ksdata: data parsed from the kickstart file and set in the
                       installation process
        @type ksdata: pykickstart.base.BaseHandler instance
        @param instclass: distribution-specific information
        @type instclass: pyanaconda.installclass.BaseInstallClass

        """

        # no actions needed in this addon
        pass

    def execute(self, storage, ksdata, instclass, users):
        """
        The execute method that should make changes to the installed system. It
        is called only once in the post-install setup phase.

        @see: setup
        @param users: information about created users
        @type users: pyanaconda.users.Users instance

        """

        hello_file_path = os.path.normpath(ROOT_PATH + HELLO_FILE_PATH)
        with open(hello_file_path, "w") as fobj:
            fobj.write("%s\n" % self.text)
