from catanatron.game import Game
from catanatron.models.player import RandomPlayer, Color, SimplePlayer, Player
from catanatron.players.weighted_random import WeightedRandomPlayer
from catanatron_experimental.machine_learning.players.mcts import MCTSPlayer
from catanatron.json import GameEncoder
from catanatron_gym.features import create_sample_vector, create_sample
from catanatron_experimental.play import play_batch
from catanatron_server.utils import open_link
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np



# %%
colors = [
   Color.RED,
   Color.BLUE,
   Color.WHITE,
   Color.ORANGE
]

def plotter():
   players = [
      WeightedRandomPlayer(colors[0]),
      WeightedRandomPlayer(colors[1]),
      WeightedRandomPlayer(colors[2]),
      WeightedRandomPlayer(colors[3]),
   ]


   trials = 10000
   data = np.zeros((trials,4))
   itera = {
      'RED':0,
      'BLUE':0,
      'WHITE':0,
      'ORANGE':0
   }

   x = np.arange(trials)
   flag = False
   i = 0

   while i < trials:
      game = Game(players)
      c = game.play()  # returns winning color
      try:
         itera[c.value] += 1
      except:
         i -= 1
         continue
      
      if c.value == 'RED':
         data[i][0] = itera[c.value]
      elif c.value == 'BLUE':
         data[i][1] = itera[c.value]
      elif c.value == 'WHITE':
         data[i][2] = itera[c.value]
      else:
         data[i][3] = itera[c.value]
      
      if flag:
         for j in range(4):
            if data[i][j] == 0:
               data[i][j] = data[i-1][j]
      flag = True
      i += 1
      
   fig, ax = plt.subplots()
   ax.plot(x,data)
   ax.legend(['Seat 1', 'Seat 2', 'Seat 3', 'Seat 4'])
   fig.show()
   print(data[-1]/trials)


# %%
