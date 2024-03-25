class Props():

    def __init__(self):
        pass

        # temporary test prop
        env = loader.load_model('environment.egg')
        env.reparent_to(base.main_render)

        panda = loader.load_model('panda.egg')
        panda.reparent_to(base.main_render)

        base.main_cam.set_pos_hpr((9.61, -13.21, 11.23), (29.221, -8.14, 0))
    
    def cleanup(self):
        pass
