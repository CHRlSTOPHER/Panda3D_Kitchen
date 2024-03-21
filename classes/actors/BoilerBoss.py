from direct.actor.Actor import Actor

from classes.settings import Globals as G

ROOM_PATH = G.DOM_5 + "ttr_m_ara_crg_boiler"
ACTOR_PATH = G.CHAR_5 + "ttr_r_chr_cbg_boss" + G.BAM
ACTOR_PARENT = "loc_boss"
ELEVATOR_PARENTS = ['exit1_loc', 'exit2_loc', 'elevator_loc']

DESK_PARENT = "loc_desk"
DESK = "Desk"
DESKS = 16

SMALL_PARENT = "loc_smallB"
SMALL = "SmallB"
SMALLS = 6 # The number of pipes.


class BoilerBoss(Actor):

    def __init__(self, name="~boiler"):
        Actor.__init__(self)
        self.room = None
        self.desks = []
        self.smalls = []

        self.load_boiler()
        self.load_desks()
        self.set_name(name)

        render.analyze()

    def load_boiler(self):
        self.room = loader.load_model(ROOM_PATH + G.BAM)
        self.room.reparent_to(render)
        self.room.flatten_strong()

        boiler_pos = self.room.find(f'**/{ACTOR_PARENT}').get_pos()
        self.load_model(ACTOR_PATH)
        self.reparent_to(render)
        self.set_pos(boiler_pos)

    def load_desks(self):
        desk_path = f'{ROOM_PATH}' + DESK + G.BAM
        desk = loader.load_model(desk_path)
        for desk_num in range(0, DESKS):
            desk.copy_to(self.room.find(f'**/{DESK_PARENT}{desk_num}'))