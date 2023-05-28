# Machine Learning Toolbox 2 - MLTB2

[![MIT License](https://img.shields.io/github/license/telekom/mltb2)](https://github.com/telekom/mltb2/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/mltb2)](https://www.python.org)
[![pypi](https://img.shields.io/pypi/v/mltb2.svg)](https://pypi.python.org/pypi/mltb2)
<br/>
[![pytest](https://github.com/telekom/mltb2/actions/workflows/pytest.yml/badge.svg)](https://github.com/telekom/mltb2/actions/workflows/pytest.yml)
[![Static Code Checks](https://github.com/telekom/mltb2/actions/workflows/static_checks.yml/badge.svg)](https://github.com/telekom/mltb2/actions/workflows/static_checks.yml)
[![GitHub issues](https://img.shields.io/github/issues-raw/telekom/mltb2)](https://github.com/telekom/mltb2/issues)

📦 A box of machine learning tools. 📦

## Main Components

[`from mltb2.somajo import SoMaJoSentenceSplitter`](https://github.com/telekom/mltb2/blob/main/mltb2/somajo.py)\
Split texts into sentences. For German and English language.
This is done with the [SoMaJo](https://github.com/tsproisl/SoMaJo) tool.

[`from mltb2.transformers import TransformersTokenCounter`](https://github.com/telekom/mltb2/blob/main/mltb2/transformers.py)\
Count tokens made by a [Transformers](https://github.com/huggingface/transformers) tokenizer.

[`from mltb2.somajo_transformers import TextSplitter`](https://github.com/telekom/mltb2/blob/main/mltb2/somajo_transformers.py)\
Split the text into sections with a specified maximum token length.
Does not divide words, but always whole sentences.

[`from mltb2.optuna import SignificanceRepeatedTrainingPruner`](https://github.com/telekom/mltb2/blob/main/mltb2/optuna.py)\
An [Optuna pruner](https://optuna.readthedocs.io/en/stable/reference/pruners.html)
to use statistical significance (a t-test which serves as a heuristic) to stop
unpromising trials early, avoiding unnecessary repeated training during cross validation.

## Installation

MLTB2 is available at [the Python Package Index (PyPI)](https://pypi.org/project/mltb2/).
It can be installed with pip:

```bash
pip install mltb2
```

Some optional dependencies might be necessary. You can install all of them with:

```bash
pip install mltb2[optional]
```

## Licensing

Copyright (c) 2023 Philip May\
Copyright (c) 2023 Philip May, Deutsche Telekom AG

Licensed under the **MIT License** (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License by reviewing the file
[LICENSE](https://github.com/telekom/mltb2/blob/main/LICENSE) in the repository.
