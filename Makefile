src := mltb2
other-src := tests docs

check:
	poetry run black $(src) $(other-src) --check --diff
	poetry run mypy --install-types --non-interactive $(src) $(other-src)
	poetry run ruff check $(src) $(other-src)
	poetry run mdformat --check --number .
	poetry run make -C docs clean doctest

format:
	poetry run black $(src) $(other-src)
	poetry run ruff check $(src) $(other-src) --fix
	poetry run mdformat --number .

test:
	poetry run pytest $(other-src)

sphinx:
	poetry run make -C docs clean html

open-sphinx:
	open docs/build/html/index.html

install:
	poetry lock && poetry install --all-extras
