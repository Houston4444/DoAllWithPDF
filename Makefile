#!/usr/bin/make -f
# Makefile for Do DoAllWithPDF Service Menu #
# ---------------------- #
# Created by houston4444
#

PREFIX  = /usr/local
DESTDIR =

LINK      = ln -s
PYUIC    ?= pyuic5
PYRCC    ?= pyrcc5
LRELEASE ?= lrelease

# -----------------------------------------------------------------------------------------------------------------------------------------

# all: RES UI LOCALE
all: UI LOCALE

# -----------------------------------------------------------------------------------------------------------------------------------------
# # Resources
# 
# RES: src/resources_rc.py
# 
# src/resources_rc.py: resources/resources.qrc
# 	$(PYRCC) $< -o $@

# -----------------------------------------------------------------------------------------------------------------------------------------
# UI code

UI: doallwithpdf

doallwithpdf: src/ui_order_dialog.py src/ui_terminalDialog.py

src/ui_%.py: resources/ui/%.ui
	$(PYUIC) $< -o $@

# -----------------------------------------------------------------------------------------------------------------------------------------
# # Translations Files

LOCALE: locale

locale: locale/doallwithpdf_fr_FR.qm locale/doallwithpdf_it_IT.qm

locale/%.qm: locale/%.ts
	$(LRELEASE) $< -qm $@
# -----------------------------------------------------------------------------------------------------------------------------------------

clean:
# 	rm -f *~ src/*~ src/*.pyc src/ui_*.py src/resources_rc.py
	rm -f *~ src/*~ src/*.pyc src/ui_*.py locale/*.qm
# -----------------------------------------------------------------------------------------------------------------------------------------

debug:
	$(MAKE) DEBUG=true

# -----------------------------------------------------------------------------------------------------------------------------------------

install:
	# Create directories
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -d $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/
	install -d $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/src/
	install -d $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/houston-servicemenu-commons/
	install -d $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/book/
	install -d $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/book/UI/
	install -d $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/locale/
	install -d $(DESTDIR)$(PREFIX)/share/kservices5/ServiceMenus/DoAllWithPDF/
	
# 	# Install script files and binaries
	install -m 755 data/doallwithpdf_servicemenu      $(DESTDIR)$(PREFIX)/bin/
	install -m 755 data/notifier.py                   $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/
	install -m 755 data/houston-servicemenu-commons/* $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/houston-servicemenu-commons/
	install -m 755 data/book/book_helper.py           $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/book/
	install -m 755 data/book/bookorder.py             $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/book/
	install -m 755 data/book/UI/*                     $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/book/UI/
	
	#install Translations
	install -m 655 locale/*.qm                        $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/locale/
	
	# Install servicemenu files
	install -m 655 data/ServiceMenus/*                $(DESTDIR)$(PREFIX)/share/kservices5/ServiceMenus/DoAllWithPDF/

	# Install main code
	install -m 755 src/doallwithpdf_servicemenu.py $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/src/
	install -m 755 src/*.py $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/src/
	
# 	We'll need it later !!!
# 	# Adjust PREFIX value in script file
# 	sed -i "s?X-PREFIX-X?$(PREFIX)?" $(DESTDIR)$(PREFIX)/bin/doallwithpdf_servicemenu

# -----------------------------------------------------------------------------------------------------------------------------------------

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/doallwithpdf_servicemenu
	rm -rf $(DESTDIR)$(PREFIX)/share/DoAllWithPDF/
	rm -rf $(DESTDIR)$(PREFIX)/share/kservices5/ServiceMenus/DoAllWithPDF/
