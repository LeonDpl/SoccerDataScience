# SoccerDataScience

## Work

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
        - Plot player / team metric aggregated per game over time
      - Stack : which db?, flask, streamlit?

## Formalisation

- Key Performance Metrics
  - **xG** : Expected Goals, the probability of a shot resulting in a goal (0 to 1)
  - **PPDA** : Passes Per Defensive Actions, indication of the pressing intensity, number of passes opposing team makes before a defensive action
  - **Packing** : Measure of the passing/dribbling effectiveness, the number of defenders bypassed by a pass or a dribble.
  - **EPV** : Expected Possession Value, Pass probability * Pass Value
   
 - Concepts:
   - Line breaking
   - Backward passing
   - **PI** : Pass Value
   - **PC** : Pitch control
   - **PP** : Pass probability 


## Resources

 - Unsorted links:
     - [youtube : Intro to statsbombpy API](https://www.youtube.com/watch?v=Ryn8etss1p4)
     - [paper: SFM Soccer Factor Model](https://arxiv.org/pdf/2412.05911)
     - [article: Key metrics and methods of player evaluations](https://soccerwizdom.com/2024/11/28/player-evaluations-in-soccer-key-metrics-and-methods/)
     - [article: How to evaluate player performance](https://football-observatory.com/IMG/pdf/note02en.pdf)
     - [paper: Data-Driven Visual Performance Analysis in Soccer](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2018.02416/full)
     - [lecture: EPV](https://uppsala.instructure.com/courses/28112/pages/8-expected-possession-value)
     - [paper: Actions speaks louder than goals](https://arxiv.org/pdf/1802.07127)
     - [dataset: Google Research Football with Manchester City](https://www.kaggle.com/competitions/google-football/rules)
  
 - Courses:
     - [Mathematical modelling of football](https://uppsala.instructure.com/courses/28112/pages)
  
 - Repos:
   - [FoTD](https://github.com/Friends-of-Tracking-Data-FoTD)
   - [StatsBomb open data](https://github.com/statsbomb/open-data/tree/master/data)


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

### StatsBomb

- [repo: StatsBombPy](https://github.com/statsbomb/statsbombpy)
  - `pip install statsbombpy`