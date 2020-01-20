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

"""This module contains constants that are used by various parts of the addon."""

from dasbus.identifier import DBusServiceIdentifier
from pyanaconda.core.dbus import DBus
from pyanaconda.modules.common.constants.namespaces import ADDONS_NAMESPACE

# These define location of the addon's service on D-Bus. See also the data/*.conf file.

HELLO_WORLD_NAMESPACE = (*ADDONS_NAMESPACE, "HelloWorld")

HELLO_WORLD = DBusServiceIdentifier(
    namespace=HELLO_WORLD_NAMESPACE,
    message_bus=DBus
)

# It's better to store paths without the initial slash "/" because of os.path.join behavior.
HELLO_WORLD_FILE_PATH = "root/hello_world.txt"
