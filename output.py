class OutputHandler:
  def __init__(self):
    self.s = ''
  
  def output(self, msg, line=True):
    if line:
      print(msg)
    self.s += str(msg) + '\n'

  def __str__(self):
    s = '```\n' + self.s + '```'
    self.s = ''
    return s