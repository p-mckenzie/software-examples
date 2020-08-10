# UI Example Projects

A collection of projects by Paige McKenzie, centered around building various user interfaces. 

Table of Contents
======
[Unbeatable Tic-tac-toe with Pygame](#tic-tac-toe)

<a name="tic-tac-toe"/>

## Unbeatable tic-tac-toe with Pygame
Programmed algorithm for [unbeatable](https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy) (win or, at worst, draw) 
tic-tac-toe. Implemented a CLI user interface and visual user interface using Pygame to allow a user to compete
against the AI.

See my [blog post](https://p-mckenzie.github.io/2020/07/30/tic-tac-toe/) describing the project.

Files:
```
+-- tictactoe
    --PlayCLI.py
    --PlayPygame.py
    --BaseGame.py
    +-- assets
        --o.jpg
        --tictactoe_background.jpg
        --x.jpg
        
```

Software:
Python 3.6, relying on numpy. Pygame version 1.9.6 was used for `PlayPygame.py`.