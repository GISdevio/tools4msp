import math
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
from .utils import write_to_file_field
try:
    import cartopy.io.img_tiles as cimgt
except:
    pass


# TODO: replace with
# https://gist.github.com/mappingvermont/d534539fa3ebe4a1e242644e528bf7b9
def get_zoomlevel(extent):
    GLOBE_WIDTH = 256
    west = extent[0]
    east = extent[2]
    angle = east - west
    zoom = round(math.log(300 * 360 / angle / GLOBE_WIDTH) / math.log(2))
    return zoom


def get_map_figure_size(extent, height=8.):
    width = height / (extent[3] - extent[1]) * (extent[2] - extent[0])
    return [width + 1, height]


def plot_map(raster, file_field=None, ceamaxval=None, logcolor=True, cmap="jet", coast=False, grid=True, alpha=None, vmin=None, norm=None, extend='neither',
             quantile_outliers=None):

    if quantile_outliers is not None:
        # some functions (eg. quantiles) seem to ignore mask
        # so masked values are setted to nan
        raster = raster.flattening_outliers(quantile_outliers)
        extend='max'

    fig = plt.figure(figsize=get_map_figure_size(raster.rio.bounds()))
    ax = fig.add_subplot(1, 1, 1)
    plot_norm = norm
    if logcolor:
        _vmin = vmin if (vmin is not None and vmin > 0) else 1e-6
        plot_norm = colors.LogNorm(vmin=_vmin, vmax=ceamaxval)
    mapimg = raster.plot.imshow(ax=ax,
                                cmap=cmap,
                                norm=plot_norm,
                                add_colorbar=True,
                                vmin=vmin,
                                vmax=ceamaxval)
    fig.tight_layout()

    # ax.add_image(cimgt.Stamen('toner-lite'), get_zoomlevel(raster.geobounds))
    if file_field is not None:
        write_to_file_field(file_field, plt.savefig, 'png')
        plt.clf()
        plt.close()


