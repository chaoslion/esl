.PHONY: all build clean dev docker

all: build

build: clean
	python3 setup.py build bdist_wheel

docker: build
	docker-compose build app

clean:
	python3 -m pip uninstall -y rover
	rm -rf .pytest_cache
	rm -rf build dist
	rm -rf src/rover.egg-info
	find -name __pycache__ -type d -exec rm -r {} +

dev: clean
	python3 -m pip install --user -e .
