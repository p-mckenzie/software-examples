# Software Example Projects

A collection of projects by Paige McKenzie, centered around expanding my software engineering skillset. 

Table of Contents
======
[Markov chains for text generation](#markov)

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

<a name="markov"/>

## Markov chains for text generation
Wrote adaptable program that accepts input text and uses Markov chains of various sizes
to genreate text similar to the input corpus. 

See my [blog post](https://p-mckenzie.github.io/2020/11/03/markov-chains/) describing the project.

Files:
```
+-- markov
    --generate_sentences.py
```

`generate_sentences.py` usage:

```
--filename FILENAME, -f FILENAME
                        Path to raw .txt file. If none is provided, defaults
                        to most recently-created dictionaries.
  --simulations SIMULATIONS, -s SIMULATIONS
                        the # of random sentences to build, defaults to 10
  --markovsize MARKOVSIZE, -m MARKOVSIZE
                        the # of tokens to consider when building sentences,
                        defaults to 2
  --randomseed RANDOMSEED, -r RANDOMSEED
                        the random seed to use when building sentences,
                        defaults to 1
```

Software:
Python 3.6, relying on pandas, scikit-learn, re, and NLTK.