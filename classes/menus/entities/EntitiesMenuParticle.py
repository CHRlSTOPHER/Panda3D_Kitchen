from classes.startup.DisplayRegions import swap_preview_region_in


class EntitiesMenuParticle():

    def __init__(self):
        pass

    def load_entity(self, directory):
        swap_preview_region_in(True)

    def cleanup_entity(self):
        swap_preview_region_in(False)