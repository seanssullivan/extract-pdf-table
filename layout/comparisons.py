def within_margin(actual, expected, margin):
  return True if actual <= expected + margin and actual >= expected - margin else False
