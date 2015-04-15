PYTHON=$(shell which python)
HERE=$(PWD)
ZP_DIR=$(HERE)/ZenPacks/zenoss/Docker

default: build

egg:
	python setup.py bdist_egg

build:
	python setup.py bdist_egg
	python setup.py build

clean:
	rm -rf build dist *.egg-info

analytics:
	rm -f ZenPacks/zenoss/Docker/analytics/analytics-bundle.zip
	mkdir -p analytics/resources/public/Docker_ZenPack
	./create-analytics-bundle \
		--folder="Docker ZenPack" \
		--domain="Docker Domain" \
		--device=192.168.1.205
	cd analytics; zip -r ../ZenPacks/zenoss/Docker/analytics/analytics-bundle.zip *

test:
	runtests ZenPacks.zenoss.Docker