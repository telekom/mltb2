# Copyright (c) 2021 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""Optuna specific functionality.

This module is based on `Optuna <https://optuna.readthedocs.io/en/stable/>`_.
Use pip to install the necessary dependencies for this module:
``pip install mltb2[optuna]``
"""


import logging

import numpy as np
import optuna
from optuna.pruners import BasePruner
from optuna.study import StudyDirection
from scipy import stats

_logger = logging.getLogger(__name__)


class SignificanceRepeatedTrainingPruner(BasePruner):
    """Optuna pruner which uses statistical significance as an heuristic for decision-making.

    This is an Optuna :mod:`Pruner <optuna.pruners>` which uses statistical significance as
    an heuristic for decision-making. It prunes repeated trainings like in a cross validation.
    As the test method a `t-test <https://en.wikipedia.org/wiki/Student's_t-test>`_ is used.
    Our experiments have shown that an ``aplha`` value between 0.3 and 0.4 is reasonable.

    :mod:`Optuna's standard pruners <optuna.pruners>` assume that you only adjust the model once
    per hyperparameter set. Those pruners work on the basis of intermediate results. For example,
    once per epoch. In contrast, this pruner does not work on intermediate results but on the
    results of a cross validation or more precisely the results of the individual folds.

    Below is a minimalist example:

    .. testcode::

        from mltb2.optuna import SignificanceRepeatedTrainingPruner
        import logging
        import numpy as np
        import optuna
        from sklearn.datasets import load_iris
        from sklearn.model_selection import StratifiedKFold
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score

        # configure the logger to see the debug output from the pruner
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.getLogger("mltb2.optuna").setLevel(logging.DEBUG)

        dataset = load_iris()

        x, y = dataset['data'], dataset['target']

        def train(trial):
            parameter = {
                'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
                'n_estimators': trial.suggest_int('n_estimators', 20, 100),
            }

            validation_result_list = []

            skf = StratifiedKFold(n_splits=10)
            for fold_index, (train_index, val_index) in enumerate(skf.split(x, y)):
                X_train, X_val = x[train_index], x[val_index]
                y_train, y_val = y[train_index], y[val_index]

                rf = RandomForestClassifier(**parameter)
                rf.fit(X_train, y_train)
                y_pred = rf.predict(X_val)

                acc = accuracy_score(y_val, y_pred)
                validation_result_list.append(acc)

                # report result of this fold
                trial.report(acc, fold_index)

                # check if we should prune
                if trial.should_prune():
                    # prune here - we are done with this CV
                    break

            return np.mean(validation_result_list)

        study = optuna.create_study(
            # storage="sqlite:///optuna.db",  # we use in-memory storage here
            study_name="iris_cv",
            direction="maximize",
            load_if_exists=True,
            sampler=optuna.samplers.TPESampler(multivariate=True),
            # add pruner to optuna
            pruner=SignificanceRepeatedTrainingPruner(
                alpha=0.4,
                n_warmup_steps=4,
            )
        )

        study.optimize(train, n_trials=10)

    Args:
        alpha: The alpha level for the statistical significance test.
            The larger this value is, the more aggressively this pruner works.
            The smaller this value is, the stronger the statistical difference between the two
            distributions must be for Optuna to prune.
            ``alpha`` must be ``0 < alpha < 1``.
            Our experiments have shown that an ``aplha`` value between 0.3 and 0.4 is reasonable.
        n_warmup_steps: Pruning is disabled until the trial reaches or exceeds the given number
            of steps.
    """

    def __init__(self, alpha: float = 0.1, n_warmup_steps: int = 4) -> None:
        # input value check
        if n_warmup_steps < 0:
            raise ValueError("'n_warmup_steps' must not be negative! n_warmup_steps: {}".format(n_warmup_steps))
        if alpha >= 1:
            raise ValueError("'alpha' must be smaller than 1! {}".format(alpha))
        if alpha <= 0:
            raise ValueError("'alpha' must be greater than 0! {}".format(alpha))

        self.n_warmup_steps = n_warmup_steps
        self.alpha = alpha

    def prune(self, study: optuna.study.Study, trial: optuna.trial.FrozenTrial) -> bool:  # noqa: D102
        # get best tial - best trial is not available for first trial
        best_trial = None
        try:
            best_trial = study.best_trial
        except ValueError:
            pass

        if best_trial is not None:
            trial_intermediate_values = list(trial.intermediate_values.values())

            _logger.debug("trial_intermediate_values: %s", trial_intermediate_values)

            # wait until the trial reaches or exceeds n_warmup_steps number of steps
            if len(trial_intermediate_values) >= self.n_warmup_steps:
                trial_mean = np.mean(trial_intermediate_values)

                best_trial_intermediate_values = list(best_trial.intermediate_values.values())
                best_trial_mean = np.mean(best_trial_intermediate_values)

                _logger.debug("trial_mean: %s", trial_mean)
                _logger.debug("best_trial_intermediate_values: %s", best_trial_intermediate_values)
                _logger.debug("best_trial_mean: %s", best_trial_mean)

                if (trial_mean < best_trial_mean and study.direction == StudyDirection.MAXIMIZE) or (
                    trial_mean > best_trial_mean and study.direction == StudyDirection.MINIMIZE
                ):
                    pvalue = stats.ttest_ind(
                        trial_intermediate_values,
                        best_trial_intermediate_values,
                    ).pvalue

                    _logger.debug("pvalue: %s", pvalue)

                    if pvalue < self.alpha:
                        _logger.info("We prune this trial. pvalue: %s", pvalue)

                        return True

                else:
                    _logger.debug("This trial is better than best trial - we do not check for pruning.")

            else:
                _logger.debug("This trial did not reach n_warmup_steps - we do no checks.")

        return False
