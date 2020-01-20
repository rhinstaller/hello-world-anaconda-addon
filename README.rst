Hello World addon
=================

The "hello world" Anaconda addon is a minimalistic example of an addon. The code does not distract
addon developers from the vital parts of addon design. At the same time, it demonstrates Anaconda's
API and functionality provided for addons.

The actual functionality provided by the addon is creating a file ``/root/hello_world.txt`` with
custom contents on the installed system. Users can provide text for the file in GUI and Kickstart.
Besides adding the text, order of the lines can be reversed.

Changes in the addon
--------------------

This version of the addon works with Anaconda 32.19 and brings an important change where the code
no longer runs in a single process. Instead, there are now two parts: The GUI or TUI, and a worker
service. The UI and the service run each in a separate process. These two processes communicate
using D-Bus. This is the same method that Anaconda uses.

Additional information
----------------------

For information on developing addons see:
https://rhinstaller.github.io/anaconda-addon-development-guide/


File and directory overview
===========================

The following diagram explains the structure of files and directories needed for an addon. All
items of importance are explained below the diagram. The layout actually mostly follows structure
of Anaconda's code. ::

    <repository root>
    ├── data                    <1>
    ├── LICENSE
    ├── Makefile
    ├── README.rst
    └── org_fedora_hello_world  <2>
        ├── constants.py        <3>
        ├── service             <4>
        ├── categories          <5>
        ├── gui                 <6>
        └── tui                 <7>

The directories and files seen here are:

1. Files needed to configure and run the D-Bus service
2. Directory for actual Python code of the addon
3. Constants shared by the service and GUI code
4. Code that runs as a stand-alone D-Bus service/process
5. Code that describes how to integrate the GUI or TUI into Anaconda's interface
6. Code for graphical interface
7. Code for text interface

In most cases, you can assume that ``HelloWorld``, ``hello_world`` and other variations of
"hello world" are specific to this addon and will need changing for your own addon.

Service files
-------------

The files in the ``data`` directory are needed to configure and run the D-Bus service in the
installation environment. These are:

``org.fedoraproject.Anaconda.Addons.HelloWorld.conf``
    Configuration for D-Bus that describes the objects on the bus and access rights to these.

``org.fedoraproject.Anaconda.Addons.HelloWorld.service``
    A D-Bus service file that describes the D-Bus service to be started. Note that even though
    these files have the same ``.service`` extension as ``systemd`` unit files and use a similar
    format, they are different and are not parsed by ``systemd`` but rather the D-Bus daemon.

For more information about D-Bus service file syntax, see the D-Bus specification:
https://dbus.freedesktop.org/doc/dbus-specification.html#message-bus-starting-services

The name of the directory is not required by any rule, but make sure to adjust the ``Makefile``
if you change the name.

Makefile
--------

The ``Makefile`` provided with this addon is very basic. It copies files to their respective paths,
and then creates an updates image that contains these files.

The paths for the various types of files encoded in the ``Makefile`` are required by Anaconda.
If you put your own files anywhere else, the addon will not work.

For more information about the updates image created by ``Makefile``, see
https://fedoraproject.org/wiki/Anaconda/Updates

Addon code directory
--------------------

All Python code of the addon should be placed in an ``<addon_name>`` directory. Anaconda addons
generally use for this directory a naming scheme that concatenates hierarchically nested
identifiers into an URL-like string. You can read ``org_fedora_hello_world`` as the three
components: ``org``, ``fedora``, and ``hello_world``. You should create your own namespace for
your addon, eg. ``com_example_widgets``.

In the Python code, the name of this directory corresponds to where your modules are located:

>>> from org_fedora_hello_world.foo.bar import baz

In this example addon, this directory contains a single file:

``constants.py``
    This file contains constants needed by both the D-Bus service and the user interface code.

Other files shared by both interface and service can go here too, or have their own directory.
This part of the tree is not accessed by anything else than your addon's code, so you are free to
make up your own rules.

D-Bus service code
------------------

Code in the ``<addon_name>/service`` is what runs as the D-Bus service. The path to this directory
is not required by any rule, but make sure to adjust the ``Makefile`` and configuration in
``dbus_data`` to match. Additionally, the need to share code between the service and UI means you
need to have the directory with the service code somewhere under the ``<addon_name>`` directory.

The files found here are:

``kickstart.py``
    Implements classes needed to handle Kickstart data:
    Parse Kickstart text into internal data structures, and vice versa.

``hello_world.py``
    Implements the class that represents the D-Bus service. Binds together the whole service.

``hello_world_interface.py``
    Implements an interface for the D-Bus service class.
    Thanks to the ``dasbus`` library, this then automatically becomes the actual D-Bus interface.

``installation.py``
    Implements ``Task`` classes that perform actual work.

``__main__.py``
    A Python script that actually runs the D-Bus service.
    The D-Bus service file starts this code using a shell script supplied with Anaconda.

The naming of these files is only a soft convention, and follows how Anaconda's own code is laid
out. If you understand the structure well enough, you can change these at will.

Interface code
--------------

The code for the addon's user interfaces (integrated into Anaconda's user interfaces) follows
a rigid structure: ::

    org_fedora_hello_world/
    ├── categories
    │   └── hello_world.py
    ├── gui
    │   └── spokes
    │       ├── hello_world.glade
    │       └── hello_world.py
    └── tui
        └── spokes
            └── hello_world.py

The files are the following:

``categories/hello_world.py``
    Provides "category" classes added by the addon, if needed. A category is a group of spokes
    (screens). In GUI, a category is visualized as a heading; the icons and text to enter spokes
    are grouped under these heading.

    The Hello World addon creates its own category to demonstrate this, and thus contains this file.
    Other addons may not need this.

    The name of this file is arbitrary, but it's a good practice to name it after your addon.

``gui/spokes/hello_world.py``
    Provides a class that implements the GUI variant of the spoke (screen).
    This class handles converting internal data to GUI controls and back.

    The name of this file is arbitrary. You can have multiple spokes in one file, too.

``gui/spokes/hello_world.glade``
    Provides a definition of the GUI structure.
    Create this with the Glade application supplied with GNOME.

    It is a very good idea to name the GUI files same as the Python modules, and have one file
    per one screen. However, the name of this file and how many of these you have is very
    arbitrary: One glade file can contain multiple screens, and the code for each spoke can specify
    which screen it uses.

``tui/spokes/hello_world.py``
    Provides a class that implements the TUI variant of the spoke.
    The same considerations as for the GUI variant apply.

__init__.py files
-----------------

To let Python recognize your modules, you will need several ``__init__.py`` files.
If you do not know how to use these, put one in every directory under ``<addon_name>``.
