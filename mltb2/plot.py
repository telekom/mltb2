# Copyright (c) 2018 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""A collection of plot tools.

This module is based on `Matplotlib <https://matplotlib.org/>`_.
Use pip to install the necessary dependencies for this module:
``pip install mltb2[plot]``
"""

from typing import Optional

import matplotlib.pyplot as plt


# see https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.twinx.html
def twin_axes_timeseries_plot(
    values_1,
    label_1: str,
    values_2,
    label_2: str,
    start_timestep_number: int = 0,
    shift_1: int = 0,
    shift_2: int = 0,
    title: Optional[str] = None,
    label_x: str = "Step",
    color_1: str = "tab:red",
    color_2: str = "tab:blue",
):
    """Create twin axes timeseries plot.

    Plots two different timeseries curves in one diagram but two different y-axes.
    This function does not call `matplotlib.pyplot.plot()`.

    Args:
        values_1: (``array_like``) Values for the first timeseries curve.
        label_1: Label for the first timeseries curve.
        values_2: (``array_like``) Values for the second timeseries curve.
        label_2: Label for the second timeseries curve.
        start_timestep_number: Number for first point in time. Default is 0.
        shift_1: Number of timesteps to shift the first timeseries curve.
            Can be positive or negative. Default is 0.
        shift_2: Number of timesteps to shift the second timeseries curve.
            Can be positive or negative. Default is 0.
        title: Title of the plot.
        label_x: Label for the x-axis (timeseries axis). Default is 'Step'.
        color_1: Color of first timeseries curve. Default is 'tab:red'.
        color_2: Color of second timeseries curve. Default is 'tab:blue'.
    """
    fig, ax1 = plt.subplots()

    if title is not None:
        plt.title(title)

    ax1.set_xlabel(label_x)

    ax1.set_ylabel(label_1, color=color_1)
    ax1.plot(
        range(start_timestep_number + shift_1, len(values_1) + start_timestep_number + shift_1),
        values_1,
        color=color_1,
    )
    ax1.tick_params(axis="y", labelcolor=color_1)

    ax2 = ax1.twinx()

    ax2.set_ylabel(label_2, color=color_2)
    ax2.plot(
        range(start_timestep_number + shift_2, len(values_2) + start_timestep_number + shift_2),
        values_2,
        color=color_2,
    )
    ax2.tick_params(axis="y", labelcolor=color_2)

    # otherwise the labels might be slightly clipped
    # see https://matplotlib.org/users/tight_layout_guide.html
    fig.tight_layout()


def boxplot(values, labels=None, title=None, xlabel=None, ylabel=None, vert=True):
    """Prints one or more boxplots in a single diagram.

    This function does not call `matplotlib.pyplot.plot()`.
    """
    _, ax = plt.subplots()

    if title is not None:
        ax.set_title(title)

    if xlabel is not None:
        ax.set(xlabel=xlabel)

    if ylabel is not None:
        ax.set(ylabel=ylabel)

    ax.boxplot(values, labels=labels, vert=vert)

    if vert:
        grid_axis = "y"
    else:
        grid_axis = "x"

    plt.grid(b=True, axis=grid_axis, linestyle="--")

    plt.xticks(rotation=90)


def boxplot_dict(values_dict, title=None, xlabel=None, ylabel=None, vert=True):
    """Create boxplot form dictionary.

    This function does not call `matplotlib.pyplot.plot()`.
    """
    values = []
    labels = []

    for key, value in values_dict.items():
        values.append(value)
        labels.append(key)

    boxplot(values, labels=labels, title=title, xlabel=xlabel, ylabel=ylabel, vert=vert)


def save_last_figure(filename):
    """Saves the last plot.

    For jupyter notebooks this has to be called in the same cell that created the plot.
    """
    plt.savefig(filename, bbox_inches="tight")
