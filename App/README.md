# Soccer Data Science

> [!NOTE]
> Soccer Data Science Application is a streamlit web application for desktop use (UI not designed for mobile interface)
> App is available on streamlit's cloud at : https://dle-soccerdatascience.streamlit.app/

## Description 
The app aims at exploring soccer data from different sources : 
- Event data : StatsBomb

Objectives of the application is to provide insights of games, players, tactics in order to understand key indicators of performances how they impact game results.

### Available features

- Match Insight
  - Load an ensemble of games for a specific team
  - Display the games according to some characteristics
    - [x] Goal average
    - [x] Centrality
    - [ ] xG
  - Display lineups
    - [x] List players per team
    - [ ] Order players by game time
    - [ ] Display tactics on the pitch
  - Events Analysis
    - [x] Heatmap of the events with filters
    - [ ] Boxplot of events per player (differenciate teams)
    - [ ] Boxplot of events per position (differenciate teams)
  - Pass Analysis
    - Display game metrics
      - [x] Centrality
      - [ ] Number of pass
      - [ ] Number of successfull pass
      - [ ] Distribution of successfull pass length
    - [x] Display pass graph
  - Shot analysis

## ToDo
Here is a list of unsorted tasks and ideas to improve the application

- Add Application logo
- Rework multi-pages behaviour https://discuss.streamlit.io/t/rename-the-home-page-in-a-multi-page-app/65533/3
- Store computed metrics in a SQLite database (centrality for instance) to improve loading performance
  - Set-up an api (Flask) to get metrics from the DB
- Generate a description of the metrics directly onto the application, with reading guidelines
- Work on use cases and how the application answer to these problems
- 

