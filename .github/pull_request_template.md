## Description

<!-- Please describe your pull request here. -->

## Pull request checklist

- tests
  - [ ] Do we have tests? Should we add more?
  - [ ] Should we parametrize tests?
  - [ ] Should we add hypothesis tests?
- documentation
  - [ ] add docstrings
  - [ ] if a module is new: add API reference file for Sphinx in `docs/source/api-reference`
  - [ ] check API doc of Sphinx - build and show with `make sphinx && make open-sphinx`
- [ ] fix checks
  - start locale checks with `make check`
  - fix formatting with `make format`
- Python type info
  - [ ] check and improve Python type info
  - [ ] double check if return types are specified - including `-> None`
- [ ] check TODO comments in code
- [ ] check FIXME comments in code
- [ ] check if we want to increase the version or rc number
- [ ] check if the copyright needs an update
  - file header
  - README.md
  - LICENSE file
