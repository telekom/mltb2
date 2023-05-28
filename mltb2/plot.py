# Copyright (c) 2018 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""A collection of plot tools."""

import matplotlib.pyplot as plt


# see https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.twinx.html
def twin_axes_timeseries_plot(
    values_1,
    label_1,
    values_2,
    label_2,
    start_timestep_number=0,
    shift_1=0,
    shift_2=0,
    title=None,
    label_x="Step",
    color_1="tab:red",
    color_2="tab:blue",
):
    """Create twin axes timeseries plot.

    Plots two different timeseries curves in one diagram but two different y-axes.
    This function does not call `matplotlib.pyplot.plot()`.
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
