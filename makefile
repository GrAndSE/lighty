test:
	python setup.py test

clean:
	rm -r build

build:
	python setup.py build

install:
	$(MAKE) build
	python setup.py install

.PHONY: test
