# Connect 4 
Connect 4 programmed in python using pygame.

#### About the game: Connect 4
Connect-Four is a two-player 6x7 board game where colored discs are dropped vertically down occupying the last available slot within that respective column by taking turns by the players. When we introduce so called "**Artificial intelligence**" into the game (the agent) we we need to equip the agent with knowledge regarding states, actions and goal (goal test) in order for the agent to achieve it's goal. 

Environments have various properties and in the case of connect 4, the game's environmental properties are **Accessible**, **Deterministic**, **Static** and **Discrete**. There are many approaches that can be employed to solve the Connect-Four game based on the various algorithms, but almost all algorithms have to follow the **zero-sum** [game theory concept](https://en.wikipedia.org/wiki/Zero-sum_game) where "the total utility score is divided among the players. An increase in one player's score results in decrease in another player's score". This results in an environment which can be represented like this:

<img src="docs/image/Connect 4 - State Action.jpeg" height="500" width="500">

The basic flow of the game can be represented like this:

<img src="docs/image/Connect 4 Game Flow.jpeg" height="500" width="500">

#### The game can be played in the following manner:
* player vs player 
* player vs bot
* bot vs bot

#### The game currently has 5 bots 
1. Random Int Bot (`random`)
2. One-Step Look Ahead Bot (`onestep`)
3. MiniMax Bot (`minimax`)
4. ExpectiMax Bot (`expectimax`)
5. MonteCarlo Tree Search (`montecarlo`)

#### Features in the game:
- can play in various game mode with UI 
- can view performacne of algorithms with or without UI
- ability to choose bots based on `CLI` args
(example `python game.py --p1 minimax --p2 montecarlo --ui false`)
    - `--p1`: To select Player 1 Bot.
    - `--p2`: To select Player 2 Bot.
    - `--ui`: Accepts a boolean value to hide UI incase of bot vs bot
    - `--bots`: To list all the Available Bots.

# To run game on your machine:
1. clone the repo: `git clone https://github.com/mukeshmk/cs7is2-ai-group-proj.git`
2. create a virtual environment inside the folder: `python -m venv .venv`
3. activate the virtual environment: `.venv\Scripts\activate` (in case of Windows)
4. install the required packages for the game to run using: `pip install -r requirements.txt`
5. run the game: `python game.py`
6. make sure to `deactivate` once your done.

Basic game code taken from: [@KeithGalli](https://github.com/KeithGalli) from the repo [Connect4-Python](https://github.com/KeithGalli/Connect4-Python)

#### This game was done as part of Trinity College Dublin's CS7IS2 - Artificial intelligence Modules's - Group Project
* The project report can be found [here](docs/FIRSTNAME_LASTNAME_CS7IS2_2019_Final_Report_tex.pdf)
* The evaluation metrics and reports can be found [here](docs/results/Evaluation.xlsx)
* The win-ratio and comparison between agents can be found [here](docs/results/Win ratio between bots.xlsx)
* The reference papers and articles used in the project report can be found [here](docs/references/)

#### Contributors
 [![](https://github.com/mukeshmk.png?size=50)](https://github.com/mukeshmk) | [![](https://github.com/Aishwarya2345.png?size=50)](https://github.com/Aishwarya2345) | [![](https://github.com/Manasimohan.png?size=50)](https://github.com/Manasimohan) | [![](https://github.com/jagadishr12.png?size=50)](https://github.com/jagadishr12) 
 --- | --- | --- | --- 
 Mukesh A | Aishwarya R | Manasi M N | Jagadish R
