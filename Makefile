TMPDIR := $(shell mktemp -d)
OUTDIR := $(shell pwd)

_default:
	@mkdir -p $(TMPDIR)/usr/share/anaconda/addons/
	@cp -par org_fedora_hello_world $(TMPDIR)/usr/share/anaconda/addons/
	@cd $(TMPDIR) ; find ./usr/share/anaconda/addons/ | cpio -c -o --quiet | gzip -9 > $(OUTDIR)/hello_world_addon_updates.img
	@rm -rf $(TMPDIR)
	@echo "Put hello_world_addon_updates.img up where you can use it via"
	@echo "  inst.updates=<path>/hello_world_addon_updates.img"
