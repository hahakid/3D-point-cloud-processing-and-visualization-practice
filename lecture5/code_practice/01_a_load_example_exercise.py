import pyvista as pv
from pyvista import examples

pint_roots = examples.download_pine_roots()
print(pint_roots)
pint_roots.plot()  # 植物树根？

bolt_nut = examples.download_bolt_nut()
print(bolt_nut)
# bolt_nut.plot()  # 螺栓和螺母
pl = pv.Plotter()
_ = pl.add_volume(
    bolt_nut,
    cmap="coolwarm",   # color map
    opacity="sigmoid_5",  # opacity mapping
    show_scalar_bar=True,
)
pl.camera_position = [(194.6, -141.8, 182.0), (34.5, 61.0, 32.5), (-0.229, 0.45, 0.86)]
pl.show()