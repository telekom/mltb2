src := mltb2
test-src := tests
other-src := setup.py docs

check:
	poetry run black $(src) $(test-src) --check --diff
	poetry run mypy --install-types --non-interactive $(src) $(test-src)
	poetry run ruff $(src) $(test-src)
	poetry run mdformat --check --number .
	poetry run make -C docs clean doctest

format:
	poetry run black $(src) $(test-src)
	poetry run ruff $(src) $(test-src) --fix
	poetry run mdformat --number .

test:
	poetry run pytest $(test-src)

sphinx:
	poetry run make -C docs clean html

install:
	poetry lock && poetry install --all-extras
