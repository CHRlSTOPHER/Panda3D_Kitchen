
class Props():

    def __init__(self):
        print('loading props')
        self.room = loader.load_model('phase_9/models/cogHQ/ttr_m_ara_shq_resistanceHideout.bam')
        self.room.reparent_to(render)
        self.room.set_pos_hpr(49.53, 87.23, -24.08, -181.88, 9.0, 6.0)
        # camera.set_pos_hpr(1.19, 4.16, 1.48, -200.37, 10.88, 7.09)
        # self.room.hide()
        base.camLens.set_fov(45.0)
    
    def cleanup(self):
        self.room.remove_node()
