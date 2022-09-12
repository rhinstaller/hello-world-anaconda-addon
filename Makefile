TMPDIR := $(shell mktemp -d)
OUTDIR := $(shell pwd)

BASEDIR := $(TMPDIR)/usr/share/anaconda/
ADDONDIR := $(BASEDIR)/addons/
SERVICESDIR := $(BASEDIR)/dbus/services/
CONFDIR := $(BASEDIR)/dbus/confs/
CONTAINER_NAME = hello-world-anaconda-addon-ci

_default: updates

.PHONY: updates
updates:
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

.PHONY: container-test
container-test:
	podman build --tag $(CONTAINER_NAME) --file ./Dockerfile
	podman run --volume .:/hello-world-anaconda-addon:Z $(CONTAINER_NAME) make test

.PHONY: test
test: check

.PHONY: check
check:
	@echo "*** Running pylint checks ***"
	pylint org_fedora_hello_world/
	@echo "[ OK ]"
