from panda3d.core import Camera, NodePath, MouseWatcher

SCENE_REGION = [.3156, .9833, .3046, .9713]
PREVIEW_REGION = [.462, .8365, .3046, .9713]


def swap_preview_region_in(preview):
    if preview:
        base.preview_region.set_dimensions(*PREVIEW_REGION)
        base.main_region.set_dimensions(0, 0, 0, 0)
    else:
        base.preview_region.set_dimensions(0, 0, 0, 0)
        base.main_region.set_dimensions(*SCENE_REGION)


class KitchenDisplayRegions():

    def __init__(self):
        self.center_region = None
        self.main_cam = None
        self.main_render = None
        self.main_mouse_watcher = None

        # Bottom Left region
        self.preview_region = None
        self.preview_cam = None
        self.preview_render = None
        self.preview_mouse_watcher = None

        self.load_center_region()
        self.load_bottom_left_region()

    def load_center_region(self):
        # First, make display region that will render the main scene
        self.center_region = base.win.makeDisplayRegion(*SCENE_REGION)

        # Second, we need a camera for the new display region
        main_cam_node = Camera('main_cam')
        self.main_cam = NodePath(main_cam_node)
        self.center_region.setCamera(self.main_cam)

        # Third, define the main area nodes will be reparented object too.
        self.main_render = NodePath('main_render')
        self.main_cam.reparent_to(self.main_render)

        # Fourth, add a mouse watcher to use for node selector/fov scroll
        self.main_mouse_watcher = MouseWatcher()
        base.mouseWatcher.get_parent().attach_new_node(
            self.main_mouse_watcher)
        self.main_mouse_watcher.set_display_region(self.center_region)

        # Fifth, fix display region aspect ratio.
        aspect_ratio = base.get_aspect_ratio()
        self.main_cam.node().get_lens().set_aspect_ratio(aspect_ratio)

    def load_bottom_left_region(self):
        # This will be used for when we want to take screenshots
        # of actors, props, and particle effects.
        self.preview_region = base.win.make_display_region(0, 0, 0, 0) # hide

        preview_cam_node = Camera('preview_cam')
        self.preview_cam = NodePath(preview_cam_node)
        self.preview_cam.node().get_lens().set_fov(35)

        self.preview_render = NodePath('preview_render')
        self.preview_cam.reparent_to(self.preview_render)
        self.preview_cam.node().get_lens().set_aspect_ratio(1)
        self.preview_region.setCamera(self.preview_cam)

        self.preview_mouse_watcher = MouseWatcher()
        base.mouseWatcher.get_parent().attach_new_node(
                            self.preview_mouse_watcher)
        self.preview_mouse_watcher.set_display_region(self.preview_region)

        # debug test
        env = loader.load_model('environment.egg')
        env.reparent_to(self.preview_render)

    def get_center_region(self):
        return self.center_region

    def get_main_cam(self):
        return self.main_cam

    def get_main_mw(self):
        return self.main_mouse_watcher

    def get_main_render(self):
        return self.main_render

    def get_preview_region(self):
        return self.preview_region

    def get_preview_cam(self):
        return self.preview_cam

    def get_preview_mw(self):
        return self.preview_mouse_watcher

    def get_preview_render(self):
        return self.preview_render