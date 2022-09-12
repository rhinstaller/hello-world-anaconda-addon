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
#
# NOTE: Anaconda is using Simpleline library for Text User Interface.
#       To learn how to use Simpleline look on the documentation:
#
#       http://python-simpleline.readthedocs.io/en/latest/
#


"""Module with the class for the Hello world TUI spoke."""

import logging
import re

from simpleline.render.prompt import Prompt
from simpleline.render.screen import InputState
from simpleline.render.containers import ListColumnContainer
from simpleline.render.widgets import CheckboxWidget, EntryWidget

from pyanaconda.core.constants import PASSWORD_POLICY_ROOT
from pyanaconda.ui.tui.spokes import NormalTUISpoke
from pyanaconda.ui.common import FirstbootSpokeMixIn
# Simpleline's dialog configured for use in Anaconda
from pyanaconda.ui.tui.tuiobject import Dialog, PasswordDialog

# the path to addons is in sys.path so we can import things from org_fedora_hello_world
from org_fedora_hello_world.categories.hello_world import HelloWorldCategory
from org_fedora_hello_world.constants import HELLO_WORLD

log = logging.getLogger(__name__)

# export only the HelloWorldSpoke and HelloWorldEditSpoke classes
__all__ = ["HelloWorldSpoke", "HelloWorldEditSpoke"]

# import gettext
# _ = lambda x: gettext.ldgettext("hello-world-anaconda-plugin", x)

# will never be translated
_ = lambda x: x
N_ = lambda x: x


class HelloWorldSpoke(FirstbootSpokeMixIn, NormalTUISpoke):
    """
    Class for the Hello world TUI spoke that is a subclass of NormalTUISpoke. It
    is a simple example of the basic unit for Anaconda's text user interface.
    Since it is also inherited form the FirstbootSpokeMixIn, it will also appear
    in the Initial Setup (successor of the Firstboot tool).

    :see: pyanaconda.ui.tui.TUISpoke
    :see: pyanaconda.ui.common.FirstbootSpokeMixIn
    :see: simpleline.render.widgets.Widget
    """

    ### class attributes defined by API ###

    # category this spoke belongs to
    category = HelloWorldCategory

    def __init__(self, *args, **kwargs):
        """
        Create the representation of the spoke.

        :see: simpleline.render.screen.UIScreen
        """
        super().__init__(*args, **kwargs)
        self.title = N_("Hello World")
        self._hello_world_module = HELLO_WORLD.get_proxy()
        self._container = None
        self._reverse = False
        self._lines = ""

    def initialize(self):
        """
        The initialize method that is called after the instance is created.
        The difference between __init__ and this method is that this may take
        a long time and thus could be called in a separated thread.

        :see: pyanaconda.ui.common.UIObject.initialize
        """
        super().initialize()

    def setup(self, args=None):
        """
        The setup method that is called right before the spoke is entered.
        It should update its state according to the contents of DBus modules.

        :see: simpleline.render.screen.UIScreen.setup
        """
        super().setup(args)

        self._reverse = self._hello_world_module.Reverse
        self._lines = self._hello_world_module.Lines

        return True

    def refresh(self, args=None):
        """
        The refresh method that is called every time the spoke is displayed.
        It should generate the UI elements according to its state.

        :see: pyanaconda.ui.common.UIObject.refresh
        :see: simpleline.render.screen.UIScreen.refresh
        :param args: optional argument that may be used when the screen is
                     scheduled
        :type args: anything
        """
        # call parent method to setup basic container with screen title set
        super().refresh(args)

        self._container = ListColumnContainer(
            columns=1
        )
        self._container.add(
            CheckboxWidget(
                title="Reverse",
                completed=self._reverse
            ),
            callback=self._change_reverse
        )
        self._container.add(
            EntryWidget(
                title="Hello world text",
                value="".join(self._lines)
            ),
            callback=self._change_lines
        )

        self.window.add_with_separator(self._container)

    def apply(self):
        """
        The apply method is not called automatically for TUI. It should be called
        in input() if required. It should update the contents of internal data
        structures with values set in the spoke.
        """
        self._hello_world_module.SetReverse(self._reverse)
        self._hello_world_module.SetLines(self._lines)

    def execute(self):
        """
        The execute method is not called automatically for TUI. It should be called
        in input() if required. It is supposed to do all changes to the runtime
        environment according to the values set in the spoke.
        """
        # nothing to do here
        pass

    @property
    def completed(self):
        """
        The completed property that tells whether all mandatory items on the
        spoke are set, or not. The spoke will be marked on the hub as completed
        or uncompleted according to the returned value.

        :rtype: bool
        """
        return bool(self._hello_world_module.Lines)

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
            return _("No text set")

        reverse = self._hello_world_module.Reverse

        if reverse:
            return _("Text set with {} lines to reverse").format(len(lines))
        else:
            return _("Text set with {} lines").format(len(lines))

    def input(self, args, key):
        """
        The input method that is called by the main loop on user's input.

        :param args: optional argument that may be used when the screen is
                     scheduled
        :type args: anything
        :param key: user's input
        :type key: unicode
        :return: if the input should not be handled here, return it, otherwise
                 return InputState.PROCESSED or InputState.DISCARDED if the input was
                 processed successfully or not respectively
        :rtype: enum InputState
        """
        if self._container.process_user_input(key):
            return InputState.PROCESSED_AND_REDRAW

        if key.lower() == Prompt.CONTINUE:
            self.apply()
            self.execute()
            return InputState.PROCESSED_AND_CLOSE

        return super().input(args, key)

    def _change_reverse(self, data):  # pylint: disable=unused-argument
        """Callback when user wants to switch checkbox.

        Flip state of the "reverse" parameter which is boolean.

        :param data: can be passed when adding callback in container (not used here)
        :type data: anything
        """
        self._reverse = not self._reverse

    def _change_lines(self, data):   # pylint: disable=unused-argument
        """Callback when user wants to input new lines.

        :param data: can be passed when adding callback in container (not used here)
        :type data: anything
        """
        dialog = Dialog("Lines")
        result = dialog.run()
        self._lines = result.splitlines(True)


class HelloWorldEditSpoke(NormalTUISpoke):
    """Example class demonstrating usage of editing in TUI"""

    category = HelloWorldCategory

    def __init__(self, *args, **kwargs):
        """
        :see: simpleline.render.screen.UIScreen
        """
        super().__init__(*args, **kwargs)
        self.title = N_("Hello World Edit")
        self._container = None

        # values for user to set
        self._checked = False
        self._unconditional_input = ""
        self._conditional_input = ""

    def refresh(self, args=None):
        """
        The refresh method that is called every time the spoke is displayed.
        It should update the UI elements according to the contents of
        self.data.

        :see: pyanaconda.ui.common.UIObject.refresh
        :see: simpleline.render.screen.UIScreen.refresh
        :param args: optional argument that may be used when the screen is
                     scheduled
        :type args: anything
        """
        super().refresh(args)
        self._container = ListColumnContainer(columns=1)

        self._container.add(
            CheckboxWidget(
                title="Simple checkbox",
                completed=self._checked
            ),
            callback=self._checkbox_called
        )
        self._container.add(
            EntryWidget(
                title="Unconditional text input",
                value=self._unconditional_input),
            callback=self._get_unconditional_input
        )

        # show conditional input only if the checkbox is checked
        if self._checked:
            self._container.add(
                EntryWidget(
                    title="Conditional password input",
                    value="Password set" if self._conditional_input else ""
                ),
                callback=self._get_conditional_input
            )

        self.window.add_with_separator(self._container)

    def _checkbox_called(self, data):  # pylint: disable=unused-argument
        """Callback when user wants to switch checkbox.

        :param data: can be passed when adding callback in container (not used here)
        :type data: anything
        """
        self._checked = not self._checked

    def _get_unconditional_input(self, data):  # pylint: disable=unused-argument
        """Callback when user wants to set unconditional input.

        :param data: can be passed when adding callback in container (not used here)
        :type data: anything
        """
        dialog = Dialog(
            "Unconditional input",
            conditions=[self._check_user_input]
        )
        self._unconditional_input = dialog.run()

    def _get_conditional_input(self, data):  # pylint: disable=unused-argument
        """Callback when user wants to set conditional input.

        :param data: can be passed when adding callback in container (not used here)
        :type data: anything
        """
        dialog = PasswordDialog(
            "Unconditional password input",
            policy_name=PASSWORD_POLICY_ROOT
        )
        self._conditional_input = dialog.run()

    def _check_user_input(self, user_input, report_func):
        """Check if user has wrote a valid value.

        :param user_input: user input for validation
        :type user_input: str

        :param report_func: function for reporting errors on user input
        :type report_func: func with one param
        """
        if re.match(r'^\w+$', user_input):
            return True
        else:
            report_func("You must set at least one word")
            return False

    def input(self, args, key):
        """
        The input method that is called by the main loop on user's input.

        :param args: optional argument that may be used when the screen is
                     scheduled
        :type args: anything
        :param key: user's input
        :type key: unicode
        :return: if the input should not be handled here, return it, otherwise
                 return InputState.PROCESSED or InputState.DISCARDED if the input was
                 processed successfully or not respectively
        :rtype: enum InputState
        """
        if self._container.process_user_input(key):
            return InputState.PROCESSED_AND_REDRAW
        else:
            return super().input(args, key)

    @property
    def completed(self):
        # completed if user entered something non-empty to the Conditioned input
        return bool(self._conditional_input)

    @property
    def status(self):
        return "Hidden input %s" % ("entered" if self._conditional_input else "not entered")

    def apply(self):
        # nothing to do here
        pass
