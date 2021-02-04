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
"""Hello world category module"""

from pyanaconda.ui.categories import SpokeCategory

__all__ = ["HelloWorldCategory"]

_ = lambda x: x


class HelloWorldCategory(SpokeCategory):
    """The Hello Word category.

    Class for the Hello world category. Category groups related spokes
    together. Both logically and visually (creates a box on a hub).
    Spokes reference a class of the category they should be included in.
    """

    @staticmethod
    def get_title():
        return _("HELLO WORLD")

    @staticmethod
    def get_sort_order():
        return 0
