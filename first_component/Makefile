# Makefile

install:
	uv sync

run:
	PYTHONPATH=$(shell pwd) uv run app/main.py

test:
	PYTHONPATH=$(shell pwd) uv run pytest

check_subset:
	PYTHONPATH=$(shell pwd) uv run pytest $(test)

clean:
	rm -rf .venv