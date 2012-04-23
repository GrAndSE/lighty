# You can set these variables from the command line.
SPHINXBUILD   = sphinx-build
BUILDDIR      = doc/build
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees doc/source

test:
	python ./manage.py --config tests/test.cfg test all

clean:
	rm -r build

build:
	python setup.py build

install:
	$(MAKE) build
	python setup.py install

cleandoc:
	rm -r $(BUILDDIR)

htmldoc:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

.PHONY: test
