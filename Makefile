src := mltb2
test-src := tests
other-src := setup.py docs

check:
	poetry run black $(src) $(test-src) --check --diff
	poetry run mypy --install-types --non-interactive $(src) $(test-src)
	poetry run ruff $(src) $(test-src)
	poetry run mdformat --check --number .

format:
	poetry run black $(src) $(test-src)
	poetry run ruff $(src) $(test-src) --fix
	poetry run mdformat --number .

test:
	poetry run pytest $(test-src)

sphinx:
	cd docs && $(MAKE) clean html && cd ..

install:
	poetry lock && poetry install --all-extras
