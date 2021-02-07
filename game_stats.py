class GameStats():
    '''Track Statistics for Alien Invasion.'''

    def __init__(self, ai_settings):
        '''Initialize statistics'''
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        '''Initialize statistics that can change ingame.'''
        self.ships_left = self.ai_settings.ship_limit
