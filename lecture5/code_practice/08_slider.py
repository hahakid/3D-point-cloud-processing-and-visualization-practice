import pyvista as pv

class MyCustomRoutine:
    def __init__(self, mesh) -> None:
        self.output = mesh
        self.kwargs = {
            "radius": 0.5,
            "theta_resolution": 30,
            "phi_resolution": 30,
        }

    def __call__(self, param, value):
        self.kwargs[param] = value
        self.update()

    def update(self) -> None:
        result = pv.Sphere(**self.kwargs)
        self.output.copy_from(result)

starting_mesh = pv.Sphere()
engine = MyCustomRoutine(starting_mesh)

p = pv.Plotter()
p.add_mesh(starting_mesh, show_edges=True)

p.add_slider_widget(  #
    callback=lambda value: engine("phi_resolution", int(value)),
    rng=[3, 60],  # 范围
    value=30,  # 初始值
    title="Phi Resolution",
    pointa=(0.025, 0.1),  # slider的位置
    pointb=(0.31, 0.1),  # slider的位置
    style="modern",
)
p.add_slider_widget(  #
    callback=lambda value: engine("theta_resolution", int(value)),
    rng=[3, 60],
    value=30,
    title="Theta Resolution",
    pointa=(0.35, 0.1),
    pointb=(0.64, 0.1),
    style="modern",
)
p.add_slider_widget(  # 半径调节
    callback=lambda value: engine("radius", value),
    rng=[0.1, 1.5],
    value=0.5,
    title="Radius",
    pointa=(0.67, 0.1),
    pointb=(0.98, 0.1),
    style="modern",
)
p.show()







