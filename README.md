# Sokoban Bot
Introduction to AI assignment 1  HCM University of Technology, term 211

# Abstract
This is basically a solver for Sokoban game using Breadth-first Search and A* algorithm to search state space for a solution.
Example level sets are taken from ksokoban.online, "Mini Cosmos" and "Micro Cosmos" (40 levels each)

# Algorithm :
(see more in the Sokoban.py code, where I explain the algorithm in details)
- __Breadth-first Search__: We keep generating new state that is a combination of main character's and crates' co-ordinations push it to the queue. Pop it every loop and proceed to generate more state till solution.

- __A*__: Just like above but with a heuristic, the new state is tagged with a cost function to switch to a better branch when possible.

- In both function, I use a heuristic for more feasible searching, which is the dead lock detection. So actually, the BFS is not a genuine Blind Search, but we will consider it to be a close one. (For real, blind search took so long that I nearly lose my mind waiting)

# Instruction

- import Sokoban class from Sokoban.py and call one of the run functions:

Example:
```python
  from Sokkoban import Sokoban
  
  sokoban = Sokoban()

  sokoban.run_all() #run everything, mini, micro, 80 level, both methods
  sokoban.run_all_micro() #run all micro cosmos level (40) with both methods
  sokoban.run_all_mini() #run all mini cosmos level (40) with both methods
  sokoban.run_all_bfs() #run all level (80) with BFS
  sokoban.run_all_astar() #run all level (80) with A*
  sokoban.run_one('astar','micro',1) #run Micro cosmos 1 with A*
  sokoban.run_one('bfs','mini',3) #run Mini cosmos 3 with BFS
```

- Or run the __game.exe__: (see more instruction on the slide)
- Or run the game.py:
```cmd
  python game.py
```
