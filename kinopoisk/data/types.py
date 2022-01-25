import enum


class MovieTypes(enum.Enum):
    film = 'FILM'
    video = 'VIDEO'
    tv_series = 'TV_SERIES'
    mini_series = 'MINI_SERIES'
    tv_show = 'TV_SHOW'
    all = 'ALL'


class FactTypes(enum.Enum):
    fact = 'FACT'
    blooper = 'BLOOPER'


class ImageTypes(enum.Enum):

    def __str__(self):
        return self.value


    frame = 'STILL'
    back_stage = 'SHOOTING'
    poster = 'POSTER'
    fan_art = 'FAN_ART'
    promo = 'PROMO'
    concept_art = 'CONCEPT'
    wallpaper = 'WALLPAPER'
    cover = 'COVER'
    screenshot = 'SCREENSHOT'