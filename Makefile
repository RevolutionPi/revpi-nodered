all: build

build:
	npm ci

update-all:
	npm update

show-latest-node-red:
	npm outdated node-red

clean:
	rm -rf node_modules/

security-audit:
	npm audit

start: build
	./node_modules/node-red/bin/node-red-pi
