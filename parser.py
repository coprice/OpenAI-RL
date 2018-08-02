import argparse

def check_positive(value):
  try:
    ivalue = int(value)
  except:
    raise argparse.ArgumentTypeError("'{}' is not an integer".format(value))
  if ivalue <= 0:
       raise argparse.ArgumentTypeError("{} is not a positive integer".format(value))
  return ivalue

class Parser(object):
  def __init__(self):
    self.parser = argparse.ArgumentParser()
    self.parser.add_argument("-s", default=3, type=check_positive, \
                              help="How many times you want to display your agent \
                                    playing a game. We default to 3 game simulations.")
    self.parser.add_argument("-g", default="t", choices=['t', 'f4', 'f8', 'n'], \
                              help="The game you want to test. Valid inputs are t (taxi), \
                                    f4 (frozen lake 4x4), or f8 (frozen lake 8x8). We \
                                    display taxi by default")
    self.parser.add_argument("-a", choices=['q', 'iq', 'r'], \
                              help="The type of agent to be used. Valid inputs are \
                                    q (regular Q-learning), iq (incentivized Q-learning), \
                                    or r (random). If this is not specified, simulations \
                                    are run using an optimal policy")
    self.parser.add_argument("-i", default=2500, type=check_positive, \
                              help="The number of training iterations for learning. \
                                    We default to 2500 training iterations")
    self.args = self.parser.parse_args()

    # conflicts with N-Chain
    if self.args.g == "n":
      if self.args.a == "iq":
        self.parser.error("Cannot use Incentivized Q-Learning agent for N-Chain")
      elif self.args.a == 'q' and self.args.i > 50:
        self.parser.error("Cannot use more than 50 training iterations for N-Chain. \
                           Use -i=(0,50]")
