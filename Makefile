TMPDIR := $(shell mktemp -d)
OUTDIR := $(shell pwd)

BASEDIR := $(TMPDIR)/usr/share/anaconda/
ADDONDIR := $(BASEDIR)/addons/
SERVICESDIR := $(BASEDIR)/dbus/services/
CONFDIR := $(BASEDIR)/dbus/confs/

PYTHON?=python3


_default:
	@echo "*** Building updates image ***"
	@echo -n "Working..."
	@mkdir -p $(ADDONDIR)
	@cp -par org_fedora_hello_world $(ADDONDIR)
	@mkdir -p $(SERVICESDIR)
	@cp -pa data/org.fedoraproject.Anaconda.Addons.*.service $(SERVICESDIR)
	@mkdir -p $(CONFDIR)
	@cp -pa data/org.fedoraproject.Anaconda.Addons.*.conf $(CONFDIR)
	@cd $(TMPDIR) ; find . | cpio -c -o --quiet | gzip -9 > $(OUTDIR)/hello_world_addon_updates.img
	@rm -rf $(TMPDIR)
	@echo " done."
	@echo "Put hello_world_addon_updates.img up where you can use it via"
	@echo "  inst.updates=<path>/hello_world_addon_updates.img"


.PHONY: check
check:
	@echo "*** Running pylint ***"
	$(PYTHON) -m pylint org_fedora_hello_world/
# Using git clone of Anaconda will give you import errors. In such case, run the check this way:
# PYTHONPATH=/my/anaconda/git/clone make check
