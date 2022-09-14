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

"""Module with the HelloWorldSpoke class."""

import logging

from pyanaconda.ui.gui import GUIObject
from pyanaconda.ui.gui.spokes import NormalSpoke
from pyanaconda.ui.common import FirstbootSpokeMixIn

# the path to addons is in sys.path so we can import things from org_fedora_hello_world
from org_fedora_hello_world.categories.hello_world import HelloWorldCategory
from org_fedora_hello_world.constants import HELLO_WORLD

log = logging.getLogger(__name__)

# export only the spoke, no helper functions, classes or constants
__all__ = ["HelloWorldSpoke"]

# import gettext
# _ = lambda x: gettext.ldgettext("hello-world-anaconda-plugin", x)

# will never be translated
_ = lambda x: x
N_ = lambda x: x


class HelloWorldSpoke(FirstbootSpokeMixIn, NormalSpoke):
    """
    Class for the Hello world spoke. This spoke will be in the Hello world
    category and thus on the Summary hub. It is a very simple example of a unit
    for the Anaconda's graphical user interface. Since it is also inherited form
    the FirstbootSpokeMixIn, it will also appear in the Initial Setup (successor
    of the Firstboot tool).

    :see: pyanaconda.ui.common.UIObject
    :see: pyanaconda.ui.common.Spoke
    :see: pyanaconda.ui.gui.GUIObject
    :see: pyanaconda.ui.common.FirstbootSpokeMixIn
    :see: pyanaconda.ui.gui.spokes.NormalSpoke
    """
    ### class attributes defined by API ###

    # list all top-level objects from the .glade file that should be exposed
    # to the spoke or leave empty to extract everything
    builderObjects = ["helloWorldSpokeWindow", "buttonImage"]

    # the name of the main window widget
    mainWidgetName = "helloWorldSpokeWindow"

    # name of the .glade file in the same directory as this source
    uiFile = "hello_world.glade"

    # category this spoke belongs to
    category = HelloWorldCategory

    # spoke icon (will be displayed on the hub)
    # preferred are the -symbolic icons as these are used in Anaconda's spokes
    icon = "face-cool-symbolic"

    # title of the spoke (will be displayed on the hub)
    title = N_("_Hello World")

    ### methods defined by API ###
    def __init__(self, *args, **kwargs):
        """
        Create the representation of the spoke.

        :see: pyanaconda.ui.common.Spoke.__init__
        """
        super().__init__(*args, **kwargs)
        self._hello_world_module = HELLO_WORLD.get_proxy()
        self._entry = None
        self._reverse = None

    def initialize(self):
        """
        The initialize method that is called after the instance is created.
        The difference between __init__ and this method is that this may take
        a long time and thus could be called in a separated thread.

        :see: pyanaconda.ui.common.UIObject.initialize
        """
        super().initialize()
        self._entry = self.builder.get_object("textLines")
        self._reverse = self.builder.get_object("reverseCheckButton")

    def refresh(self):
        """
        The refresh method that is called every time the spoke is displayed.
        It should update the UI elements according to the contents of
        self.data.

        :see: pyanaconda.ui.common.UIObject.refresh
        """
        lines = self._hello_world_module.Lines
        self._entry.get_buffer().set_text("".join(lines))

        reverse = self._hello_world_module.Reverse
        self._reverse.set_active(reverse)

    def apply(self):
        """
        The apply method that is called when the spoke is left. It should
        update the D-Bus service with values set in the GUI elements.
        """
        buf = self._entry.get_buffer()
        text = buf.get_text(
            buf.get_start_iter(),
            buf.get_end_iter(),
            True
        )
        lines = text.splitlines(True)
        self._hello_world_module.SetLines(lines)

        reverse = self._reverse.get_active()
        self._hello_world_module.SetReverse(reverse)

    def execute(self):
        """
        The execute method that is called when the spoke is left. It is
        supposed to do all changes to the runtime environment according to
        the values set in the GUI elements.
        """
        # nothing to do here
        pass

    @property
    def ready(self):
        """
        The ready property that tells whether the spoke is ready (can be visited)
        or not. The spoke is made (in)sensitive based on the returned value.

        :rtype: bool
        """
        # this spoke is always ready
        return True

    @property
    def completed(self):
        """
        The completed property that tells whether all mandatory items on the
        spoke are set, or not. The spoke will be marked on the hub as completed
        or uncompleted acording to the returned value.

        :rtype: bool
        """
        return bool(self._hello_world_module.Lines)

    @property
    def mandatory(self):
        """
        The mandatory property that tells whether the spoke is mandatory to be
        completed to continue in the installation process.

        :rtype: bool
        """
        # this is an optional spoke that is not mandatory to be completed
        return False

    @property
    def status(self):
        """
        The status property that is a brief string describing the state of the
        spoke. It should describe whether all values are set and if possible
        also the values themselves. The returned value will appear on the hub
        below the spoke's title.

        :rtype: str
        """
        lines = self._hello_world_module.Lines

        if not lines:
            return _("No text added")
        elif self._hello_world_module.Reverse:
            return _("Text set with {} lines to reverse").format(len(lines))
        else:
            return _("Text set with {} lines").format(len(lines))

    ### handlers ###
    def on_entry_icon_clicked(self, entry, *args):  # pylint: disable=unused-argument
        """Handler for the textEntry's "icon-release" signal."""
        entry.set_text("")

    def on_main_button_clicked(self, *args):  # pylint: disable=unused-argument
        """Handler for the mainButton's "clicked" signal."""
        # every GUIObject gets ksdata in __init__
        dialog = HelloWorldDialog(self.data)

        # show dialog above the lightbox
        with self.main_window.enlightbox(dialog.window):
            dialog.run()


class HelloWorldDialog(GUIObject):
    """
    Class for the sample dialog.

    :see: pyanaconda.ui.common.UIObject
    :see: pyanaconda.ui.gui.GUIObject
    """
    builderObjects = ["sampleDialog"]
    mainWidgetName = "sampleDialog"
    uiFile = "hello_world.glade"

    def run(self):
        """
        Run dialog and destroy its window.

        :returns: respond id
        :rtype: int
        """
        ret = self.window.run()
        self.window.destroy()
        return ret
