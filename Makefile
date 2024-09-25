all: build

build:
	npm ci

update-npm:
	npm update

update-license:
	licensed cache  || true
	licensed notices

update-all: update-npm update-license

show-latest-node-red:
	npm outdated node-red

clean:
	rm -rf node_modules/

security-audit:
	npm audit

start: build
	./node_modules/node-red/bin/node-red-pi
