import math
import statistics


def average_width(objs):
    widths = list(map(lambda obj: obj['right'] - obj['left'], objs))
    average_width = statistics.mean(widths)
    return average_width


def average_height(objs):
    heights = list(map(lambda obj: obj['top'] - obj['bottom'], objs))
    average_height = statistics.mean(heights)
    return average_height


def average_dimensions(objs):
    width = average_width(objs)
    height = average_height(objs)
    return width, height


def y_axis_center(obj):
    return (obj['top'] + obj['bottom']) / 2
  

def x_axis_center(obj):
    return (obj['right'] + obj['left']) / 2


def center_point(obj):
    return {'y': y_axis_center(obj), 'x': x_axis_center(obj)}


def center_points(objs):
    return list(map(lambda obj: center_point(obj), objs))


def margins(text):
    top = math.floor(max(list(map(lambda char: char['top'], text))))
    right = math.floor(max(list(map(lambda char: char['right'], text))))
    bottom = math.ceil(min(list(map(lambda char: char['bottom'], text))))
    left = math.ceil(min(list(map(lambda char: char['left'], text))))
    return top, right, bottom, left
