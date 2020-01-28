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
import logging

from dasbus.server.interface import dbus_interface
from dasbus.server.property import emits_properties_changed
from dasbus.typing import *  # pylint: disable=wildcard-import,unused-wildcard-import

from pyanaconda.modules.common.base import KickstartModuleInterface

from org_fedora_hello_world.constants import HELLO_WORLD

log = logging.getLogger(__name__)


@dbus_interface(HELLO_WORLD.interface_name)
class HelloWorldInterface(KickstartModuleInterface):
    """The interface for HelloWorld.

    The interface class is needed for interfacing code running within
    Anaconda's main process and code running in the D-Bus service process. The
    dasbus library will automatically set up a D-Bus interface based on these
    classes.
    """

    def connect_signals(self):
        super().connect_signals()
        self.watch_property("Reverse", self.implementation.reverse_changed)
        self.watch_property("Lines", self.implementation.lines_changed)

    @property
    def Reverse(self) -> Bool:
        """Whether to reverse order of lines in the hello world file."""
        return self.implementation.reverse

    @emits_properties_changed
    def SetReverse(self, reverse: Bool):
        self.implementation.set_reverse(reverse)

    @property
    def Lines(self) -> List[Str]:
        """Lines of the hello world file."""
        return self.implementation.lines

    @emits_properties_changed
    def SetLines(self, lines: List[Str]):
        self.implementation.set_lines(lines)
