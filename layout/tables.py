import statistics

from layout.comparisons import within_margin
from layout.dimensions import x_axis_center, y_axis_center


def calculate_row_positions(chars, margin):
  positions = set(map(lambda char: round(y_axis_center(char) / margin) * margin, chars))
  return sorted(list(positions), reverse=True)

def sort_characters_into_rows(chars, margin):
  row_positions = calculate_row_positions(chars, margin)

  rows = []
  for pos in row_positions:
    row = [char for char in chars if within_margin(y_axis_center(char), pos, margin)]
    rows.append(row)
  return rows


def sort_characters_into_columns(rows, margin):
  entries = [merge_characters_by_proximity(row, margin) for row in rows]

  column_number = 0
  max_length = max(list(map(lambda row: len(row), entries)))
  while column_number < max_length:
    right_boundries = [row[column_number]['right'] for row in entries if len(row) > column_number]
    average_right = statistics.mean(right_boundries)
    for row in entries:
      try:
        entry = row[column_number]
      except IndexError:
        entry = {'text': '', 'right': average_right}
        row.insert(column_number, entry)
        row.sort(key=lambda entry: entry['right'])
        continue
        
      if x_axis_center(entry) > average_right:
        row.insert(column_number, {'text': '', 'right': average_right})
    
    column_number += 1
    max_length = max(list(map(lambda row: len(row), entries)))

  return entries


def merge_characters_by_proximity(chars, margin):
  sorted_chars = sorted(chars, key=lambda char: char['left'])

  groups = []
  grouped_chars = []
  for char in sorted_chars:
    if len(grouped_chars) == 0:
      grouped_chars.append(char)
      continue

    prev_char = grouped_chars[-1]
    if within_margin(prev_char['right'], char['left'], margin):
      grouped_chars.append(char)
    else:
      groups.append({
        'text': ''.join(map(lambda char: char['text'], grouped_chars)),
        'left': grouped_chars[0]['left'],
        'right': grouped_chars[-1]['right']
      })
      grouped_chars = [char]

  groups.append({
        'text': ''.join(map(lambda char: char['text'], grouped_chars)),
        'left': grouped_chars[0]['left'],
        'right': grouped_chars[-1]['right']
      })
  return groups
