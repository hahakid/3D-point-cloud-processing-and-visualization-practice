
# https://docs.pyvista.org/api/core/filters


import pyvista as pv
from pyvista import examples

dataset = examples.load_uniform()
dataset.set_active_scalars("Spatial Point Data")

threshold = dataset.threshold([100, 500])
outline = dataset.outline()

p = pv.Plotter(shape=(1, 2))
p.subplot(0, 0)
p.add_mesh(dataset, color='k', show_edges=True, opacity=0.5, scalars='Spatial Point Data')
p.subplot(0, 1)
p.add_mesh(outline, color='k')
p.add_mesh(threshold)
p.camera_position = [-2, 5, 3]
p.link_views()
p.show()

contours = dataset.contour(8)
slices = dataset.slice_orthogonal()
glyphs = dataset.glyph(factor=0.001, geom=pv.Sphere(), orient=False)

p = pv.Plotter(shape=(2,2))
p.add_mesh(outline, color='k')
p.add_mesh(threshold, show_scalar_bar=False, opacity=0.5)

p.subplot(0, 1)
p.add_mesh(outline, color='k')
p.add_mesh(contours, show_scalar_bar=False, opacity=0.5)

p.subplot(1, 0)
p.add_mesh(outline, color='k')
p.add_mesh(slices, show_scalar_bar=False, opacity=0.5)

p.subplot(1, 1)
p.add_mesh(outline, color='k')
p.add_mesh(glyphs, show_scalar_bar=False, opacity=0.5)

p.link_views()
p.show()

'''
 filter chain pipeline
example:
1 First, and empty threshold filter to clean out any NaN values.
2 Use an elevation filter to generate scalar values corresponding to height.
3 Use the clip filter to cut the dataset in half.
4 Create three slices along each axial plane using the slice_orthogonal filter.
result = dataset.threshold().elevation().clip(normal="z").slice_orthogonal()
'''

result = dataset.threshold().elevation().clip(normal="z").slice_orthogonal()
p = pv.Plotter()
p.add_mesh(outline, color="k")
p.add_mesh(result, scalars="Elevation")
p.view_isometric()
p.show()

# https://zh.wikipedia.org/wiki/Perlin%E5%99%AA%E5%A3%B0
#
freq = (1, 2, 3)  # Perlin 噪声的频率
noise = pv.perlin_noise(1, freq, (0, 0, 0))
grid = pv.sample_function(noise, [0, 3.0, -0, 1.0, 0, 1.0], dim=(120, 40, 40))
out = grid.threshold(0.02)
print(out)

mn, mx = [out["scalars"].min(), out["scalars"].max()]
clim = (mn, mx * 1.8)

out.plot(
    cmap="gist_earth_r",
    background="white",
    show_scalar_bar=False,
    lighting=True,
    clim=clim,
    show_edges=False,
)