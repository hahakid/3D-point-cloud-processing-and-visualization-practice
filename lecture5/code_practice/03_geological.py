import os
import tempfile

import numpy as np
import pyvista as pv
import requests
from pyvista import examples

# path = examples.download_file("topo_clean.vtk")
topo = pv.read('../data/topo_clean.vtk')
print(topo)

def get_gcps(filename):
    """
    Helper function retrieves the Ground Control
    Points of a GeoTIFF. Note that this requires gdal.
    """
    import rasterio

    def get_point(gcp):
        return np.array([gcp.x, gcp.y, gcp.z])

    # Load a raster
    src = rasterio.open(filename)
    # Grab the Groung Control Points
    points = np.array([get_point(gcp) for gcp in src.gcps[0]])
    # Now Grab the three corners of their bounding box
    # -- This guarantees we grab the right points
    bounds = pv.PolyData(points).bounds
    origin = [bounds[0], bounds[2], bounds[4]]  # BOTTOM LEFT CORNER
    point_u = [bounds[1], bounds[2], bounds[4]]  # BOTTOM RIGHT CORNER
    point_v = [bounds[0], bounds[3], bounds[4]]  # TOP LEFT CORNER
    return origin, point_u, point_v


origin = [310967.75148705335, 4238841.045453942, 0.0]
point_u = [358682.9364281533, 4238841.045453942, 0.0]
point_v = [310967.75148705335, 4276281.98755258, 0.0]

topo.texture_map_to_plane(origin, point_u, point_v, inplace=True)

p = pv.Plotter()
p.add_point_labels(
    np.array(
        [
            origin,
            point_u,
            point_v,
        ]
    ),
    ["Origin", "Point U", "Point V"],
    point_size=5,
)

p.add_mesh(topo)
p.show(cpos="xy")

texture = pv.read_texture('../data/downsampled_Geologic_map_on_air_photo.tif')

# Now plot the topo surface with the texture draped over it
# And make window size large for a high-res screenshot
p = pv.Plotter(window_size=np.array([1024, 768]) * 3)
p.add_mesh(topo, texture=texture)
p.camera_position = [
    (337461.4124956896, 4257141.430658634, 2738.4956020899253),
    (339000.40935731295, 4260394.940646875, 1724.0720826501868),
    (0.10526647627366331, 0.2502863297360612, 0.962432190920575),
]
p.show()


