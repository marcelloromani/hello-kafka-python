.PHONY: test
test:
	uv run pytest

lint:
	uv run ruff check .


depcheck:
	uv run deptry .

ci: lint depcheck test
	@echo "Executed ci tasks."

build:
	uv build
