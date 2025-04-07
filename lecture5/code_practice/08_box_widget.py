import pyvista as pv
from pyvista import examples
'''
mesh = pv.read("../data/nefertiti.ply")  # examples.download_nefertiti()
# 选中 clip box 调整视角，仅变换box
# 选中 空白区域 调整视角，变换两者，渲染计算量增大。
p = pv.Plotter()
p.add_mesh_clip_box(mesh, color='red')
p.show(cpos=[-1, -1, 0.2])
print(p.box_clipped_meshes)
'''

# button action test
mesh = pv.Sphere()
p = pv.Plotter()
actor = p.add_mesh(mesh, show_edges=True)
def toggle_vis(flag) -> None:
    actor.SetVisibility(flag)
def toggle_wireframe(flag) -> None:
    global actor
    p.renderer.remove_actor(actor)
    actor = p.add_mesh(mesh, show_edges=flag)

button1_position = (10, 10)

offset_x = 60
offset_y = 10
text1_position = ((button1_position[0] + offset_x),
    (button1_position[1] + offset_y))
p.add_checkbox_button_widget(toggle_vis, value=True, position=button1_position)
p.add_text("Toggle Visibility", position=text1_position, font_size=12)

button2_position = (10, 70)
text2_position = ((button2_position[0] + offset_x),
    (button2_position[1] + offset_y))
p.add_checkbox_button_widget(toggle_wireframe, value=True, position=button2_position)
p.add_text("Toggle Wireframe", position=text2_position, font_size=12)

p.show()


# 多标签
colors = [
    ["ff0000", "28e5da", "0000ff"],
    ["ffff00", "c8bebe", "f79292"],
    ["fffff0", "f18c1d", "23dcaa"],
    ["d785ec", "9d5b13", "e4e0b1"],
    ["894509", "af45f5", "fff000"],
]

class SetVisibilityCallback:
    """Helper callback to keep a reference to the actor being modified."""

    def __init__(self, actor) -> None:
        self.actor = actor

    def __call__(self, state):
        self.actor.SetVisibility(state)


# Widget size
size = 50

p = pv.Plotter()

Startpos = 12
for i, lst in enumerate(colors):
    for j, color in enumerate(lst):
        actor = p.add_mesh(pv.Sphere(center=(i, j, 0)), color=color)
        # Make a separate callback for each widget
        callback = SetVisibilityCallback(actor)
        p.add_checkbox_button_widget(
            callback,
            value=True,
            position=(5.0, Startpos),
            size=size,
            border_size=1,
            color_on=color,
            color_off="grey",
            background_color="grey",
        )
        Startpos = Startpos + size + (size // 10)

p.show()
