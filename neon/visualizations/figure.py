# ----------------------------------------------------------------------------
# Copyright 2015 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

# Imports should not be a requirement for building documentation
try:
    from bokeh.plotting import figure
    from bokeh.palettes import brewer
except ImportError:
    pass


def x_label(epoch_axis):
    """
    Get the x axis label depending on the boolean epoch_axis.
    """
    return "Epoch" if epoch_axis else "Minibatch"


def cost_fig(cost_data, plot_height, plot_width, epoch_axis=True):
    """
    Generate a figure with lines for each element in cost_data.
    """

    fig = figure(plot_height=plot_height,
                 plot_width=plot_width,
                 title="Cost",
                 x_axis_label=x_label(epoch_axis),
                 y_axis_label="Cross Entropy Error (%)")

    # Spectral palette supports 3 - 11 distinct colors
    num_colors_required = len(cost_data)
    assert num_colors_required <= 11, "Insufficient colors in predefined palette."
    colors = brewer["Spectral"][max(3, len(cost_data))]
    if num_colors_required < 3:
        # manually adjust pallette for better contrast
        colors[0] = brewer["Spectral"][6][0]
        if num_colors_required == 2:
            colors[1] = brewer["Spectral"][6][-1]

    for name, x, y in cost_data:
        fig.line(x, y, legend=name, color=colors.pop(0), line_width=2)
    return fig


def hist_fig(hist_data, plot_height, plot_width, x_range=None, epoch_axis=True):
    """
    Generate a figure with an image plot for hist_data, bins on the Y axis and
    time on the X axis.
    """
    name, hdata, dh, dw, bins, offset = hist_data
    if x_range is None:
        x_range = (0, dw)
    fig = figure(plot_height=plot_height,
                 plot_width=plot_width,
                 title=name,
                 x_axis_label=x_label(epoch_axis),
                 x_range=x_range,
                 y_range=(offset, offset + bins))
    fig.image(image=[hdata], x=[0],  y=[offset], dw=[dw], dh=[dh], palette="Spectral11")
    return fig
