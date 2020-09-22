def simplify_characters(characters):
  return list(map(lambda char: {
    'text': char.get_text(),
    'top': char.y1,
    'right': char.x1,
    'bottom': char.y0,
    'left': char.x0},
    characters))
