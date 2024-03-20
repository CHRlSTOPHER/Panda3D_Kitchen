
class Props():

    def __init__(self, _render, editor):
        print('loading props')
        self.render = _render
        self.editor = editor

        # temporary test prop
        env = loader.load_model('environment.egg')
        env.reparent_to(self.render)

        panda = loader.load_model('panda.egg')
        panda.reparent_to(self.render)
    
    def cleanup(self):
        pass
