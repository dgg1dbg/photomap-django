import random
from django.contrib.gis.geos import Polygon
import math
from django.core.cache import cache

GRID_SIZE = 0.1
MAX_GRID_PICTURES = 20

def get_grid_keys(request):
    west = float(request.GET.get('west'))
    east = float(request.GET.get('east'))
    north = float(request.GET.get('north'))
    south = float(request.GET.get('south'))

    min_x = math.floor(west / GRID_SIZE)
    max_x = math.floor(east / GRID_SIZE)
    min_y = math.floor(south / GRID_SIZE)
    max_y = math.floor(north / GRID_SIZE)

    grid_keys = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            grid_keys.append(f"grid:{x}:{y}")

    return grid_keys

def get_grid_pictures(grid_key):
    from .model import Picture
    x = int(grid_key.split(':')[1])
    y = int(grid_key.split(':')[2])
    west = x * GRID_SIZE
    east = (x + 1) * GRID_SIZE
    south = y * GRID_SIZE
    north = (y + 1) * GRID_SIZE
    polygon = Polygon.from_bbox((west, south, east, north))
    pictures = list(Picture.objects.filter(location__within=polygon))
    if len(pictures) > MAX_GRID_PICTURES:
        pictures = random.sample(pictures, MAX_GRID_PICTURES)
    return pictures

def get_cached_grid_data(grid_key):
    from .serializer import PictureViewResponseSerializer
    def load_data():
        pictures = get_grid_pictures(grid_key)
        if not pictures:
            return []
        serializer = PictureViewResponseSerializer(pictures, many=True)
        return serializer.data

    return cache.get_or_set(grid_key, load_data, timeout=60*60*24)

def get_grid_key_from_point(point):
    lon = point.x
    lat = point.y
    x = int(lon / GRID_SIZE)
    y = int(lat / GRID_SIZE)
    return f"grid:{x}:{y}"