class Tile:
    '''Типы клеток и их характеристики'''
    def __init__(self, name):
        self.name = name
        self.file_path = f'{tiles_path}{name}.png'

tiles_path = 'static/tiles/'

tiles = {
    "FOW" : Tile("FOW"),
    "bush" : Tile("bush"),
    "grass" : Tile("grass"),
    "stone" : Tile("stone"),
    "water" : Tile("water")
}