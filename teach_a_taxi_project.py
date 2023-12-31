# -*- coding: utf-8 -*-
"""Teach_A_Taxi_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-JCTiQbS_p6FXdN58trkk0WRuwB2xA8v
"""

!pip install cmake 'gym[atari]' scipy
!pip install pyglet==1.2.4
!pip install gym[toy_text]

import gym
env = gym.make("Taxi-v3").env

env.reset()
env.render()
print("Action Space {}".format(env.action_space))
print("State Space {}".format(env.observation_space))

state=env.encode(3,1,2,0)
print("State:",state)
env.s=state
env.render()
env.P[state] #Reward Table

#Without Reinforcement Learning
env.s=328
epochs=0
rewards,penalties=0,0
frames=[]  #for animation
done=False
while not done:
  action=env.action_space.sample()
  state,reward,done,info=env.step(action)
  if reward==-10:
    penalties+=1

  frames.append(
      {
          'frame':env.render(mode='ansi'),
          'state':state,
          'action':action,
          'reward':reward
      }
  )
  epochs+=1
print("Timesteps Taken:{}".format(epochs))
print("Penalties Incurred:{}".format(penalties))

from IPython.display import clear_output
from time import sleep
def print_frames(frames):
  for i,frame in enumerate(frames):
    clear_output(wait=True)
    print(frame.get('frame'))
    print(f"Timestep:{i+1}")
    print(f"state:{frame['state']}")
    print(f"Action:{frame['action']}")
    print(f"Reward:{frame['reward']}")
    sleep(.1)
print_frames(frames)

import numpy as np
import random
from IPython.display import clear_output
q_table=np.zeros([env.observation_space.n,env.action_space.n])
q_table
alpha=0.1
gamma=0.6
epsilon=0.1
all_epochs=[]
all_penalties=[]
for i in range(1,100001):
  state=env.reset()
  epochs,penalties,rewards=0,0,0
  done=False
  while not done:
    if random.uniform(0,1)<epsilon:
      action=env.action_space.sample()
    else:
      action=np.argmax(q_table[state])

    next_state,reward,done,info=env.step(action)
    old_value=q_table[state,action]
    next_max=np.max(q_table[next_state])
    new_value=(1-alpha)*old_value+alpha*(reward+gamma*next_max)
    q_table[state,action]=new_value
    if reward==-10:
      penalties+=1
    state=next_state
    epochs+=1
  if i%100==0:
    clear_output(wait=True)
    print(f"Episode:{i}")
print("Training Finished")

q_table[328]

total_epochs, total_penalties = 0, 0
episodes = 100

for _ in range(episodes):
    state = env.reset()
    epochs, penalties, reward = 0, 0, 0
    done = False
    while not done:
        action = np.argmax(q_table[state])
        state, reward, done, info = env.step(action)
        if reward == -10:
            penalties += 1
        epochs += 1
    total_penalties += penalties
    total_epochs += epochs
print(f"Results after {episodes} episodes:")
print(f"Average timesteps per episode: {total_epochs / episodes}")
print(f"Average penalties per episode: {total_penalties / episodes}")