import pyvista as pv
from pyvista import examples

mesh = examples.load_nut()
p = pv.Plotter(shape=(1, 5))
p.subplot(0, 0)
p.add_mesh(mesh)

#平滑 VTK Phong shading algorithm
p.subplot(0, 1)
p.add_mesh(mesh, smooth_shading=True)

#
p.subplot(0, 2)
p.add_mesh(mesh, smooth_shading=True, split_sharp_edges=True)

p.subplot(0, 3)
edges = mesh.extract_feature_edges(boundary_edges=False, non_manifold_edges=False, feature_angle=30, manifold_edges=False)
p.add_mesh(edges, smooth_shading=True, split_sharp_edges=True)

p.subplot(0, 4)
p.add_mesh(mesh, color="r",
           split_sharp_edges=True,
           pbr=True,
           metallic=0.5,
           roughness=0.5)

p.link_views()
p.show()




