class Parse:
  def __init__(self,init_cmds,cmds):
    self.init_cmds = init_cmds
    self.cmds = cmds
    self.fi = dict()
    self.use = self.reconstruct()
  
  def reconstruct(self):
    new_dict = dict()
    for key, value in self.init_cmds.items():
      new_dict[key.lower()] = value
    return new_dict
    
  def parse(self):
    if ',' in self.cmds:
      cmds = list(self.cmds.split(','))
      for co in cmds:
        if '=' in co:
          key, va = co.split('=')
          if key.lower() == 'del' and va != 'all' and va in self.use:
            del self.use[va]
          elif key.lower() == 'del' and va == 'all':
            self.use.clear()
          else:
            self.fi[key.lower()] = va
    else:
      if '=' in self.cmds:
        key, va = self.cmds.split('=')
        if key.lower() == 'del' and va != 'all' and va in self.use:
          del self.use[va]
        elif key.lower() == 'del' and va == 'all':
          self.use.clear()
        else:
          self.fi[key.lower()] = va
    return self.execute()
          
  def execute(self):
    if self.fi:
      for k, v in self.fi.items():
        self.use[k.lower()] = v
      self.use.pop('del', None)
    return self.use

if __name__=='__main__':
  pass