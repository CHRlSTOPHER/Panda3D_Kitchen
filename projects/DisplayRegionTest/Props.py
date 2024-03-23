class Props():

    def __init__(self):
        pass

        # temporary test prop
        env = loader.load_model('environment.egg')
        env.reparent_to(base.main_render)

        env = loader.load_model('environment.egg')
        # env.reparent_to(base.preview_render)

        panda = loader.load_model('panda.egg')
        panda.reparent_to(base.main_render)
    
    def cleanup(self):
        pass
