import numpy as np
from gaits import helix, sidewind, windowed_helix
from matplotlib import artist, patches, text
from matplotlib import pyplot as plt
from matplotlib.transforms import IdentityTransform
from mpl_toolkits.mplot3d import axes3d  # noqa: F401
from scipy.spatial.transform import Rotation

default_module_length = 2.25


def get_module_tfs(joint_angles, module_length):
    ts = [np.eye(4)]
    angles_spiraled = [pow(-1,int(i/2))*joint_angles[i] for i in range(len(joint_angles))]
    # the "twisting" rotation from vectors in frame i to i+1
    R_y = np.array([[0,0,-1],[0,1,0],[1,0,0]])
    for a in angles_spiraled:
        R_x = np.mat([[1,0,0],
                      [0,np.cos(a),np.sin(a)],
                      [0,-np.sin(a),np.cos(a)]])
        T = np.eye(4)
        T[0:3,0:3] = R_y * R_x
        T[0:3,3] = np.array([0,module_length,0])
        ts.append(ts[-1] @ T)
    return np.array(ts)

class ItemProperties:
    def __init__(self, fontsize=14, labelcolor='black', bgcolor='yellow',
                 alpha=1.0):
        self.fontsize = fontsize
        self.labelcolor = labelcolor
        self.bgcolor = bgcolor
        self.alpha = alpha


class MenuItem(artist.Artist):
    padx = 5
    pady = 5

    def __init__(self, fig, labelstr, props=None, hoverprops=None,
                 on_select=None):
        super().__init__()
        self.labelstr = labelstr
        self.props = props if props is not None else ItemProperties()
        self.hoverprops = (
            hoverprops if hoverprops is not None else ItemProperties())
        if self.props.fontsize != self.hoverprops.fontsize:
            raise NotImplementedError(
                'support for different font sizes not implemented')

        self.on_select = on_select
        self.hover = False

        # Setting the transform to IdentityTransform() lets us specify
        # coordinates directly in pixels.
        self.label = text.Text(0, 0, labelstr, transform=IdentityTransform(),
                              size=self.props.fontsize)
        self.label.set_figure(fig)
        self.text_bbox = self.label.get_window_extent(
            fig.canvas.get_renderer())

        self.rect = patches.Rectangle((0, 0), 1, 1)  # Will be updated later.

        self.set_hover_props(False)

    def setup_events(self):
        self.release_event = fig.canvas.mpl_connect('button_release_event', self.check_select)

    def remove(self):
        # 1. Disconnect the canvas click listener
        if self.figure is not None and self.release_event is not None:
            self.figure.canvas.mpl_disconnect(self.release_event)
            self.release_event = None

        # 3. Remove MenuItem itself from fig.artists
        super().remove()
        self.figure = None

    def check_select(self, event):
        over, _ = self.rect.contains(event)
        if not over:
            return
        if self.on_select is not None:
            self.on_select(self)

    def set_extent(self, x, y, w, h, depth):
        self.rect.set(x=x, y=y, width=w, height=h)
        self.label.set(position=(x + self.padx, y + depth + self.pady/2))
        self.hover = False

    def draw(self, renderer):
        self.rect.draw(renderer)
        self.label.draw(renderer)

    def set_hover_props(self, b):
        props = self.hoverprops if b else self.props
        self.label.set(color=props.labelcolor)
        self.rect.set(facecolor=props.bgcolor, alpha=props.alpha)

    def set_hover(self, event):
        """
        Update the hover status of event and return whether it was changed.
        """
        b, _ = self.rect.contains(event)
        changed = (b != self.hover)
        if changed:
            self.set_hover_props(b)
        self.hover = b
        return changed


class ParamItem(MenuItem):
    padx = 5
    pady = 5

    def __init__(self, fig, labelstr, value, props=None, hoverprops=None):
        super().__init__(fig, labelstr, props, hoverprops)
        self.value = value
        self.tempValue = value
        self.click_x = None
        self.isInt = isinstance(value, int)
        self.dragging = None
        self.update_value()

    def setup_events(self):
        super().setup_events()
        self.pressed_event = fig.canvas.mpl_connect('button_press_event', self.check_pressed)


    def remove(self):
        # 1. Disconnect the canvas click listener
        if self.figure is not None and self.release_event is not None:
            self.figure.canvas.mpl_disconnect(self.pressed_event)
            if self.dragging:
                self.figure.canvas.mpl_disconnect(self.dragging)
            self.pressed_event = None
            self.dragging = None

        super().remove()

    def check_select(self, event):
        if not self.dragging:
            return
        self.value = self.tempValue
        self.figure.canvas.mpl_disconnect(self.dragging)

    def check_pressed(self, event):
        over, _ = self.rect.contains(event)
        if not over:
            return
        self.click_x = event.x
        self.dragging = self.figure.canvas.mpl_connect('motion_notify_event', self.on_move)

    def update_value(self):
        self.label.set_text(f"{self.labelstr} = {self.tempValue}")

    def on_move(self, event):
        diff = (event.x - self.click_x) / 50.0
        if self.isInt:
            diff = int(diff)
        self.tempValue = self.value + diff
        self.update_value()

class Menu:
    def __init__(self, fig, menuitems, x0, y0):
        self.figure = fig
        self.x0 = x0
        self.y0 = y0
        self.yLast = y0
        self.menuitems = []
        self.set_items(menuitems)

        fig.canvas.mpl_connect('motion_notify_event', self.on_move)

    def set_items(self, menuitems):

        for item in self.menuitems:
            item.remove()
        del self.menuitems[:]
        self.menuitems += menuitems

        maxw = max(item.text_bbox.width for item in menuitems)
        maxh = max(item.text_bbox.height for item in menuitems)
        depth = max(-item.text_bbox.y0 for item in menuitems)

        width = maxw + 2*MenuItem.padx
        height = maxh + MenuItem.pady
        self.yLast = self.y0
        for item in menuitems:
            left = self.x0
            bottom = self.yLast - maxh - MenuItem.pady

            item.set_extent(left, bottom, width, height, depth)

            self.figure.add_artist(item)
            self.yLast -= maxh + MenuItem.pady

            item.setup_events()
        
        self.figure.canvas.draw_idle()

    def on_move(self, event):
        self.figure.canvas.draw_idle()


fig = plt.figure()
fig.subplots_adjust(left=0.3)
props = ItemProperties(labelcolor='black', bgcolor='yellow',
                       fontsize=7, alpha=0.2)
hoverprops = ItemProperties(labelcolor='white', bgcolor='blue',
                            fontsize=7, alpha=0.2)
dragprops = ItemProperties(labelcolor='black', bgcolor='green',
                            fontsize=7, alpha=0.2)

gaits = {
    'helix': (helix, {
        'module_length': default_module_length,
        'radius': 6.0,
        'pitch': 6.0,
        'time_frequency': 0.25,
    }),
    'windowed_helix': (windowed_helix, {
        'window_n': 0.0,
        'bend_angle':np.pi,
        'module_length': default_module_length,
        'radius': 6.0,
        'pitch': 6.0,
        'time_frequency': 0.25,
    }),
    'sidewind': (sidewind, {
        'amplitude_h': 0.49,
        'amplitude_v': 0.38,
        'spatial_frequency': 1/8,
        'time_frequency': 1,
    }),
}

menuitems = []
selected = None
for label in gaits:
    def on_select(item):
        global selected
        params = list(gaits[item.labelstr][1].items())
        params = [ParamItem(fig, key, value, props, dragprops) for key, value in params]
        params = [module_length, phase, n_modules] + params
        param_menu.set_items(params)
        selected = item.labelstr
        print(f'you selected {item.labelstr}')
    item = MenuItem(fig, label, props=props, hoverprops=hoverprops,
                    on_select=on_select)
    menuitems.append(item)

menu = Menu(fig, menuitems, 10, 470)

module_length = ParamItem(fig, 'new_module_length', 2.25, props=props, hoverprops=dragprops)
phase = ParamItem(fig, 'phase', 0.0, props=props, hoverprops=dragprops)
n_modules = ParamItem(fig, 'n_modules', 16, props=props, hoverprops=dragprops)
param_menuitems = [module_length, phase, n_modules]
param_menu = Menu(fig, param_menuitems, 10, menu.yLast - 10)

ax = fig.add_subplot(1,2,1,projection='3d')

# Prepare arrays x, y, z
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)

line, = ax.plot(x, y, z, label='parametric curve')
center_a, = ax.plot([0,0],[0,0],[0,0], label='debug center')
center_b, = ax.plot([0,0],[0,0],[0,0], label='debug center')
ax.legend()

# ax2 = fig.add_subplot(1,2,2)
# x_plot, = ax2.plot([0,1], [0,1], c="red")
# y_plot, = ax2.plot([0,1], [0,1], c="green")
# z_plot, = ax2.plot([0,1], [0,1], c="blue")

def helix_line_from_params(pitch, radius, n_modules, module_length, phase, time_frequency):

    angle = np.arctan(pitch / (radius * np.pi * 2))
    height = n_modules * module_length * pitch / np.sqrt(
        (2 * np.pi * radius) ** 2 + pitch**2
    )
    line = np.array([
        [0, 0 , 0, 1],
        [height, 0 , 0, 1],
    ])
    T_helix = np.eye(4)
    T_helix[:3,:3] = Rotation.from_euler('z', angle).as_matrix()
    T_helix[2,3] = radius
    T_phase = np.eye(4)
    T_phase[:3,:3] = Rotation.from_euler('y', phase * np.pi * 2 * time_frequency).as_matrix()
    line = (T_phase @ T_helix @ line.T).T
    # Set fourth column to phase
    p = pitch / (2 * np.pi)
    spatial_frequency = (module_length * p) / (p**2 + radius**2)
    line[0,3] = 0
    line[1,3] = phase + n_modules * spatial_frequency  / (np.pi * 2) / time_frequency
    return line

def ax_on_move(event):
    if selected is None:
        return
    params = {}
    for item in param_menu.menuitems:
        params[item.labelstr] = item.tempValue
    l = params['new_module_length']
    del params['new_module_length']
    ratio = l / params['module_length']
    new_n_modules = int(params['n_modules'] / ratio)
    for key in ['spatial_frequency', 'amplitude', 'amplitude_h', 'amplitude_v']:
        if key in params:
            params[key] *= ratio
    if 'window_n' in params:
        params['window_n'] /= ratio
    if 'module_length' in params:
        params['module_length'] = l
    params['n_modules'] = new_n_modules
    tfs = get_module_tfs(gaits[selected][0](**params), l)
    points = tfs[:,0:3,3]
    # xyzs = []
    # T_y = np.eye(4)
    # for tf in tfs:
    #     T_y @= np.array([[0,0,1,0],[0,1,0,0],[-1,0,0,0], [0,0,0,1]])
    #     xyzs.append(Rotation.from_matrix((tf @ T_y)[:3,:3]).as_euler('xyz', degrees=True))
    # xyzs = np.array(xyzs)
    # x_plot.set_data(range(len(xyzs)), xyzs[:,0])
    # y_plot.set_data(range(len(xyzs)), xyzs[:,1])
    # z_plot.set_data(range(len(xyzs)), xyzs[:,2])
    # ax2.relim()
    # ax2.autoscale()

    if 'window_n' in params:
        # angle = np.arctan(params['pitch'] / (params['radius'] * np.pi * 2))
        window_mask = [i >= params['window_n'] for i in range(params['n_modules'])]
        window_index = window_mask.index(True)
        # Front helix is offset in phase to produce bend.
        phase_offset = params['bend_angle'] # * np.sign(amplitude * spatial_frequency)
        # Phase is normalized from 0-1 and also depends on time frequency
        phase_offset /=  2 * np.pi * params['time_frequency']
        points_a = helix_line_from_params(
            params['pitch'], 
            params['radius'], 
            window_index, 
            params['module_length'], 
            params['phase'] + phase_offset, 
            params['time_frequency']
        )
        points_b = helix_line_from_params(
            params['pitch'], 
            params['radius'], 
            params['n_modules'] - window_index, 
            params['module_length'], 
            points_a[1,3] - phase_offset, 
            params['time_frequency']
        )
        # points_center = np.vstack([points_a, points_b])
        # T_y = np.eye(4)
        # for i in range(window_index % 4):
        #     T_y @= np.array([[0,0,1,0],[0,1,0,0],[-1,0,0,0], [0,0,0,1]])
        # points_center = (tfs[window_index] @ T_y @ points_center.T).T
        # roll, pitch, yaw = Rotation.from_matrix((tfs[window_index] @ T_y)[:3,:3]).as_euler('xyz', degrees=True)
        # print(yaw)
        # # 1. Update X and Y data
        center_a.set_data(points_a[:,0], points_a[:,1])
        # 2. Update Z data separately (required for 3D plots)
        center_a.set_3d_properties(points_a[:,2])
        # # 1. Update X and Y data
        center_b.set_data(points_b[:,0], points_b[:,1])
        # 2. Update Z data separately (required for 3D plots)
        center_b.set_3d_properties(points_b[:,2])
    # Center points in graph
    # points -= np.mean(points, axis=0)

    curr_x = ax.get_xlim()
    curr_y = ax.get_ylim()
    curr_z = ax.get_zlim()

    x_min = np.min([curr_x[0], np.min(points)])#[:,0])])
    x_max = np.max([curr_x[1], np.max(points)])#[:,0])])
    y_min = np.min([curr_y[0], np.min(points)])#[:,1])])
    y_max = np.max([curr_y[1], np.max(points)])#[:,1])])
    z_min = np.min([curr_z[0], np.min(points)])#[:,2])])
    z_max = np.max([curr_z[1], np.max(points)])#[:,2])])

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_zlim(z_min, z_max)

    # 1. Update X and Y data
    line.set_data(points[:,0], points[:,1])
    # 2. Update Z data separately (required for 3D plots)
    line.set_3d_properties(points[:,2])

fig.canvas.mpl_connect('motion_notify_event', ax_on_move)

plt.show()
