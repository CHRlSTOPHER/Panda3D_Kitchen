from classes.actors.Toon import Toon
class Actors():

    def __init__(self, _render, editor):
        self.ai_spai = Toon(_render, head='qls', toon_name="~self.ai_spai",
                            #torso='m',
                            head_color=7, gender='f', arm_color=6,
                            bottom='skirt', names=True)
        spai_shirt = loader.load_texture('phase_4/maps/ttr_t_chr_avt_shirt_taskForceSleuth2.jpg')
        smasher_shirt = loader.load_texture('phase_4/maps/ttr_t_chr_avt_shirt_taskForceSmasher.jpg')
        spai_sleeve = loader.load_texture('phase_4/maps/ttr_t_chr_avt_shirtSleeve_taskForce.jpg')
        spai_skirt = loader.load_texture('phase_4/maps/ttr_t_chr_avt_skirt_taskForceTrainee.jpg')
        smasher_shorts = loader.load_texture('phase_4/maps/ttr_t_chr_avt_shorts_taskForceSmasher.jpg')
        self.ai_spai.find('**/torso-top').set_texture(spai_shirt, 1)
        self.ai_spai.find('**/torso-bot').set_texture(spai_skirt, 1)
        self.ai_spai.find('**/sleeves').set_texture(spai_sleeve, 1)
        self.ai_spai.disable_autowalker()
        self.ai_spai.pose('think', 49)
        glasses_texture = loader.load_texture(
            'phase_4/maps/tt_t_chr_avt_acc_msk_sellbotGlasses.jpg',
            'phase_4/maps/tt_t_chr_avt_acc_msk_sellbotGlasses_a.rgb',
        )
        glasses = "phase_4/models/accessories/tt_m_chr_avt_acc_msk_dorkGlasses.bam"
        self.ai_spai_glasses = loader.load_model(glasses)
        self.ai_spai_glasses.set_texture(glasses_texture, 1)
        self.ai_spai_glasses.reparent_to(self.ai_spai.get_part("head"))
        s = .3
        self.ai_spai_glasses.set_pos_hpr_scale(0, 0, 0, 180, -30, 0, s, s, s)
        self.ai_spai_glasses.set_pos_hpr(-0.0, 0.11, 0.2, 180.0, -61.82, 0.0)
        self.ai_spai_glasses.set_name("~self.ai_spai_glasses")

        right_elbow = self.ai_spai.control_joint(None, 'torso', 'def_right_elbow')
        left_elbow = self.ai_spai.control_joint(None, 'torso', 'def_left_elbow')
        right_elbow.set_pos_hpr(0.53, 0.0, 0.0, -71.66, -16.5, -43.5)
        left_elbow.set_pos_hpr(-0.83, -0.01, 0.18, -124.24, -34.83, -51.17)
        # editor.node_mover.set_node(left_elbow)

        t = 8
        c = 1
        self.pink = Toon(_render, 'm', "~self.pink", 1000,
                         'pss', 's', 'm', 'shorts',
                         41, 41, 41,
                         c, c, 41, c, 41, c, 41, True)
        surprise_texture = loader.load_texture(
            "phase_3/maps/eyesSurprised.jpg",
            "phase_3/maps/eyesSurprised_a.rgb",
        )
        self.pink.find('**/torso-top').set_texture(smasher_shirt, 1)
        self.pink.find('**/torso-bot').set_texture(smasher_shorts, 1)
        self.pink.find('**/sleeves').set_texture(spai_sleeve, 1)
        self.pink.disable_autowalker()

        self.pink.find('**/eyes-short').set_texture(surprise_texture, 1)
        self.pink.change_muzzle('surprise')
        self.pink.pose("duck", 20)

        self.load_attributes()

    def load_attributes(self):
        self.pink.get_part("head").set_pos_hpr(0.0, 0.0, 0.0, 42.36, 3.75,
                                               -4.5)
        self.pink.set_pos_hpr(-3.6, -3.12, 1.11, -90.89, -4.52, -0.75)
        self.pink.hide()

        # self.ai_spai.pose('toss', 20)
        self.ai_spai.get_part("head").set_pos_hpr(0.0, 0.0, 0.0, 10.5, -18.0,
                                                  9.0)
        self.ai_spai.left_eye.set_pos_hpr(-0.04, 0.0, -0.02, 0.0, 0.0, 0.0)
        self.ai_spai.right_eye.set_pos_hpr(-0.05, 0.04, -0.01, 0.0, 0.0, 0.0)
        self.ai_spai_glasses.set_pos_hpr(-0.0, 0.17, 0.2, 180.0, -58.86, -1.26)
        camera.set_pos_hpr(-1.83, 4.4, 1.51, -152.08, 10.48, -12.82)
        # self.ai_spai.set_pos_hpr(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        # self.ai_spai.hide()

        self.ai_spai.set_pos_hpr(-0.06, -0.98, 0.38, 1.73, 3.0, 4.07)
        self.ai_spai.right_eye.set_pos_hpr(-0.02, 0.03, -0.08, -2.25, 0.0, 0.0)
        self.ai_spai.left_eye.set_pos_hpr(0.02, 0.03, -0.09, 0.0, 0.0, 0.0)
        self.ai_spai.get_part("head").set_pos_hpr(0.0, 0.0, 0.0, -2.25, 3.75, -16.5)

    def cleanup(self):
        self.pink.delete()
        self.ai_spai.delete()