.PHONY: install run debug clean lint lint-strict

install:
	uv sync

run:
	uv run python -m src.fly_in $(MAP)

debug:
	uv run python -m pdb -m src.fly_in

clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache data/output output
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	uv run flake8 src/fly_in
	uv run mypy src/fly_in --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 src/fly_in
	uv run mypy src/fly_in --strict