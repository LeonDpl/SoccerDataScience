# SoccerDataScience

## Work

- 2025-06-30
  - Start a streamlit App

- 2025-06-25
  - Manipulate statsbombpy to prototype a function to get player data per game on a season

- 2025-06-21
  - Init a github repo
  - Do some research on soccer analytics, performance and domain specific knowledge
  - Init a notebook to explore Statsbomb data
  - TODO : 
    - Continue domain kowledge formalisation
      - List datasources and content and dataset samples
      - Organize state of the art related to soccer performance
    - Small app specification 
      - Expected functions:
        - Plot player / team metric over time during a game
        - ~~Plot player / team metric aggregated per game over time~~
      - Stack : which db?, flask, streamlit?

## Formalisation and Glossary

- Glossary
  - [Wyscout glossary](https://dataglossary.wyscout.com/)
  - [Soccer positions explained](https://jobsinfootball.com/blog/soccer-positions/)

- Key Performance Metrics

| Acronym | Definition | Link |
| -- | -- | -- |
| xG |  Expected Goals, the probability of a shot resulting in a goal (0 to 1) | |
| xT |  Expected Threat, for attacking actions: passes, dribbles, carries etc. | [Soccermatics](https://soccermatics.readthedocs.io/en/latest/lesson4/EvaluatingActions.html) |
| xD |  Expected Defense, for defending actions: interceptions, blocks | [Soccermatics](https://soccermatics.readthedocs.io/en/latest/lesson4/EvaluatingActions.html) |
| PPDA | Passes Per Defensive Actions, indication of the pressing intensity, number of passes opposing team makes before a defensive action | |
| Packing | Measure of the passing/dribbling effectiveness, the number of defenders bypassed by a pass or a dribble | |
| EPV | Expected Possession Value, Pass probability * Pass Value | |
| Centralisation Index | Sum the difference between maximal number of successful passes by 1 player and number of successful passes by each player divided by the sum of all passes multiplied by (number of players - 1) 
   
 - Concepts:
   - Line breaking
   - Backward passing
   - **PI** : Pass Value
   - **PC** : Pitch control
   - **PP** : Pass probability


## Resources

 - Unsorted links:
     - [youtube : Intro to statsbombpy API](https://www.youtube.com/watch?v=Ryn8etss1p4)
     - [article: Key metrics and methods of player evaluations](https://soccerwizdom.com/2024/11/28/player-evaluations-in-soccer-key-metrics-and-methods/)
     - [article: How to evaluate player performance](https://football-observatory.com/IMG/pdf/note02en.pdf)
     - [lecture: EPV](https://uppsala.instructure.com/courses/28112/pages/8-expected-possession-value)
     - [paper: Actions speaks louder than goals](https://arxiv.org/pdf/1802.07127)
     - [dataset: Google Research Football with Manchester City](https://www.kaggle.com/competitions/google-football/rules)
     - [dataset: Football analytics 101](https://football-analytics-101.readthedocs.io/en/latest/data.html)
     - [article: Luis Enrique réinvente le jeu de position au PSG](https://www.sky-sport.ch/fr/articles/5-dedans-5-dehors-luis-enrique-reinvente-le-jeu-de-position-au-psg-2/)
  
 - Courses:
     - [Mathematical modelling of football](https://uppsala.instructure.com/courses/28112/pages)
  
 - Repos:
   - [FoTD](https://github.com/Friends-of-Tracking-Data-FoTD)
   - [StatsBomb open data](https://github.com/statsbomb/open-data/tree/master/data)
   - [Soccermatics](https://soccermatics.readthedocs.io/)
  
 - Papers :
   - [Data-driven understanding on soccer team tactics and ranking trends: Elo rating-based trends on European soccer leagues](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0318485)
   - [Player Migration and Soccer Performance](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.00616/full)
   - [Football Rating Systems for Top-Level Competition: A Critical Survey](https://www.degruyterbrill.com/document/doi/10.2202/1559-0410.1071/html)
   - [Visual analytics of soccer player performance using objective ratings](https://journals.sagepub.com/doi/full/10.1177/14738716231220539)
   - [A new performance metric for player evaluation based on causality](https://statsbomb.com/wp-content/uploads/2022/09/Alessandro-Crechin-A-New-Performance-Metric-For-Player-Evaluation-Based-On-Causality.pdf)
   - [Modelling team play style using tracking data](https://statsbomb.com/wp-content/uploads/2022/09/Alessandro-Crechin-A-New-Performance-Metric-For-Player-Evaluation-Based-On-Causality.pdf)
   - [Data-Driven Visual Performance Analysis in Soccer](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2018.02416/full)
   - [SFM Soccer Factor Model](https://arxiv.org/pdf/2412.05911)


## Code

## Installation

- [Git](https://git-scm.com/downloads/win)
- [miniconda](https://www.anaconda.com/download)
- [VSCode](https://code.visualstudio.com/Download)
  - Install extensions : Python, Github issues, Jupyter
  - Create Python+Conda environment : ctrl+shift+p > Python:Environment
  - Restart VScode / Relaunch terminal

## Python set-up

- create environment : `conda create -n <envname> python=<pythonversion>`
- activate environment : `conda activate  <envname>`
- export environment yaml file : `conda env export > <envname>.yml`

## Git config and VSCode

- `git config --global user.name "<name>"`
- `git config --global user.email "<email>"`

### StatsBomb

- [repo: StatsBombPy](https://github.com/statsbomb/statsbombpy)
  - `pip install statsbombpy`
