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

"""Module with the class for the Hello world TUI spoke."""

# import gettext
# _ = lambda x: gettext.ldgettext("hello-world-anaconda-plugin", x)

# will never be translated
_ = lambda x: x
N_ = lambda x: x

import re

from pyanaconda.ui.tui.spokes import NormalTUISpoke
from pyanaconda.ui.tui.spokes import EditTUISpoke
from pyanaconda.ui.tui.spokes import EditTUISpokeEntry as Entry
from pyanaconda.ui.common import FirstbootSpokeMixIn

# export only the HelloWorldSpoke and HelloWorldEditSpoke classes
__all__ = ["HelloWorldSpoke", "HelloWorldEditSpoke"]

class HelloWorldSpoke(FirstbootSpokeMixIn, NormalTUISpoke):
    """
    Class for the Hello world TUI spoke that is a subclass of NormalTUISpoke. It
    is a simple example of the basic unit for Anaconda's text user interface.
    Since it is also inherited form the FirstbootSpokeMixIn, it will also appear
    in the Initial Setup (successor of the Firstboot tool).

    :see: pyanaconda.ui.tui.TUISpoke
    :see: pyanaconda.ui.common.FirstbootSpokeMixIn
    :see: pyanaconda.ui.tui.tuiobject.TUIObject
    :see: pyaanconda.ui.tui.simpleline.Widget

    """

    ### class attributes defined by API ###

    # title of the spoke
    title = N_("Hello World")

    # categories in text mode are simple strings that are not shown anywhere,
    # every hub just has a list of categories it should display spokes from
    # let's just use one of the standard categories defined for the Summary hub
    category = "localization"

    def __init__(self, app, data, storage, payload, instclass):
        """
        :see: pyanaconda.ui.tui.base.UIScreen
        :see: pyanaconda.ui.tui.base.App
        :param app: reference to application which is a main class for TUI
                    screen handling, it is responsible for mainloop control
                    and keeping track of the stack where all TUI screens are
                    scheduled
        :type app: instance of pyanaconda.ui.tui.base.App
        :param data: data object passed to every spoke to load/store data
                     from/to it
        :type data: pykickstart.base.BaseHandler
        :param storage: object storing storage-related information
                        (disks, partitioning, bootloader, etc.)
        :type storage: blivet.Blivet
        :param payload: object storing packaging-related information
        :type payload: pyanaconda.packaging.Payload
        :param instclass: distribution-specific information
        :type instclass: pyanaconda.installclass.BaseInstallClass

        """

        NormalTUISpoke.__init__(self, app, data, storage, payload, instclass)
        self._entered_text = ""

    def initialize(self):
        """
        The initialize method that is called after the instance is created.
        The difference between __init__ and this method is that this may take
        a long time and thus could be called in a separated thread.

        :see: pyanaconda.ui.common.UIObject.initialize

        """

        NormalTUISpoke.initialize(self)

    def refresh(self, args=None):
        """
        The refresh method that is called every time the spoke is displayed.
        It should update the UI elements according to the contents of
        self.data.

        :see: pyanaconda.ui.common.UIObject.refresh
        :see: pyanaconda.ui.tui.base.UIScreen.refresh
        :param args: optional argument that may be used when the screen is
                     scheduled (passed to App.switch_screen* methods)
        :type args: anything
        :return: whether this screen requests input or not
        :rtype: bool

        """

        self._entered_text = self.data.addons.org_fedora_hello_world.text
        return True

    def apply(self):
        """
        The apply method that is called when the spoke is left. It should
        update the contents of self.data with values set in the spoke.

        """

        self.data.addons.org_fedora_hello_world.text = self._entered_text

    def execute(self):
        """
        The excecute method that is called when the spoke is left. It is
        supposed to do all changes to the runtime environment according to
        the values set in the spoke.

        """

        # nothing to do here
        pass

    @property
    def completed(self):
        """
        The completed property that tells whether all mandatory items on the
        spoke are set, or not. The spoke will be marked on the hub as completed
        or uncompleted acording to the returned value.

        :rtype: bool

        """

        return bool(self.data.addons.org_fedora_hello_world.text)

    @property
    def status(self):
        """
        The status property that is a brief string describing the state of the
        spoke. It should describe whether all values are set and if possible
        also the values themselves. The returned value will appear on the hub
        below the spoke's title.

        :rtype: str

        """

        text = self.data.addons.org_fedora_hello_world.text
        if text:
            return _("Text set: %s") % text
        else:
            return _("Text not set")

    def input(self, args, key):
        """
        The input method that is called by the main loop on user's input.

        :param args: optional argument that may be used when the screen is
                     scheduled (passed to App.switch_screen* methods)
        :type args: anything
        :param key: user's input
        :type key: unicode
        :return: if the input should not be handled here, return it, otherwise
                 return INPUT_PROCESSED or INPUT_DISCARDED if the input was
                 processed succesfully or not respectively
        :rtype: bool|unicode

        """

        if key:
            self._entered_text = key

        # no other actions scheduled, apply changes
        self.apply()

        # close the current screen (remove it from the stack)
        self.close()
        return True

    def prompt(self, args=None):
        """
        The prompt method that is called by the main loop to get the prompt
        for this screen.

        :param args: optional argument that can be passed to App.switch_screen*
                     methods
        :type args: anything
        :return: text that should be used in the prompt for the input
        :rtype: unicode|None

        """

        return _("Enter a new text or leave empty to use the old one: ")

class _EditData(object):
    """Auxiliary class for storing data from the example EditSpoke"""

    def __init__(self):
        """Trivial constructor just defining the fields that will store data"""

        self.checked = False
        self.shown_input = ""
        self.hidden_input = ""

class HelloWorldEditSpoke(EditTUISpoke):
    """Example class demonstrating usage of EditTUISpoke inheritance"""

    title = N_("Hello World Edit")
    category = "localization"

    # simple RE used to specify we only accept a single word as a valid input
    _valid_input = re.compile(r'^\w+$')

    # special class attribute defining spoke's entries as:
    # Entry(TITLE, ATTRIBUTE, CHECKING_RE or TYPE, SHOW_FUNC or SHOW)
    # where:
    #   TITLE specifies descriptive title of the entry
    #   ATTRIBUTE specifies attribute of self.args that should be set to the
    #             value entered by the user (may contain dots, i.e. may specify
    #             a deep attribute)
    #   CHECKING_RE specifies compiled RE used for deciding about
    #               accepting/rejecting user's input
    #   TYPE may be one of EditTUISpoke.CHECK or EditTUISpoke.PASSWORD used
    #        instead of CHECKING_RE for simple checkboxes or password entries,
    #        respectively
    #   SHOW_FUNC is a function taking self and self.args and returning True or
    #             False indicating whether the entry should be shown or not
    #   SHOW is a boolean value that may be used instead of the SHOW_FUNC
    #
    #   :see: pyanaconda.ui.tui.spokes.EditTUISpoke
    edit_fields = [
        Entry("Simple checkbox", "checked", EditTUISpoke.CHECK, True),
        Entry("Always shown input", "shown_input", _valid_input, True),
        Entry("Conditioned input", "hidden_input", _valid_input,
              lambda self, args: bool(args.shown_input)),
        ]

    def __init__(self, app, data, storage, payload, instclass):
        EditTUISpoke.__init__(self, app, data, storage, payload, instclass)

        # just populate the self.args attribute to have a store for data
        # typically self.data or a subtree of self.data is used as self.args
        self.args = _EditData()

    @property
    def completed(self):
        # completed if user entered something non-empty to the Conditioned input
        return bool(self.args.hidden_input)

    @property
    def status(self):
        return "Hidden input %s" % ("entered" if self.args.hidden_input
                                    else "not entered")

    def apply(self):
        # nothing needed here, values are set in the self.args tree
        pass
