# Boss Clash

## Overview
An action 2D game where the player faces off with the boss using ball. Players can use various abilities and dashing mechanics to avoid attacks and deflect the ball from the boss to itself. The game combines simple controls with progressively more difficult boss battles.

## Project Review
A relevant existing project is boss battle game, where players face off against bosses with unique abilities. These games often have basic movement and combat systems.

- **Improvements**:
  - **Dash and Ability Skills**: Player abilities and dash skills with a cooldown to make the player manage the movement and adds a strategic layer to the gameplay. Players will need to master when to dash to avoid attacks or use their special ability to deal significant damage.
  - **Dynamic Boss Phases**: The bosses will have unique phases that change their attack patterns based on health thresholds, increasing challenge and excitement.

## Programming Development

### Game Concept  
- **Objective**:
  - The player must defeat a series of progressively stronger bosses by using their ball, abilities, and dash skills while avoiding boss attacks
- **Mechanics**:
  - The player can move, use abilities, and dash across the screen using simple controls (arrow keys for movement, spacebar for deflect,a dash key for quick movement and a unique skill ).
  - Each boss features multiple phases that change their behavior and attacks based on their remaining health.

### Object-Oriented Programming Implementation
| Class              | Responsibility                                                                                                                                |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| CharacterSelection | Manages the character selection screen, allowing the player to pick a character, enter their name, and view stats or quit the game.           |
| DataCollector      | Handles game data collection and logging for analytics such as dash usage, ability usage, playtime, boss defeats, and character selection.    |
| StatsViewer        | Manages the display and interaction with game statistics, including ability usage, boss defeats, character choices, dash usage, and playtime. |
| Player             | Manages the player’s movement, deflect, ability usage, and dash mechanics.                                                                    |
| DeflectParticle    | Draws the effect of deflect skill                                                                                                             |
| Wall               | Represents a wall that the Blue character can summon, which interacts with the ball.                                                          |
| Boss               | Handles the boss's health, behavior, and special abilities.                                                                                   |
| Lava               | Represents a lava patch created by the boss, which can damage the player if they stand on it.                                                                                                                                   |
| Fireball           |Represents a fireball fired by the boss that moves towards the player and deals damage on collision                                                                                                                                 |
| Snowball           | Represents a snowball fired by the boss that moves towards the player and deals damage on collision.                                                                                                                                  |
| Snow               |Represents snow patches on the ground. If the player steps on it, they are slowed down or frozen.                                                                                                                                |
| AnimatedHealthBar        | Represents a health bar with animation, showing the player's or boss's health status                                                                                                                                  |
| GameOverScreen         | Displays the game over screen, including buttons to retry or return to the main menu, and shows relevant game statistics like time survived and bosses defeated.                                                                                                                                  |
| Ball        |  Represents the projectile that the player deflected the ball.                                                                                                                               |
| Game         | Manages the entire game flow, including the player, boss, health bars, timer, and game over conditions. Handles input and updates the game state.                                                                                                                               |

<h2>UML Class Diagram</h2>
<img src="uml_diagram.png" >

<p><a href="uml_diagram.png"> View Full Resolution</a></p>

**Algorithms Involved**:
  - **Movement Logic**: Detects and updates player and ball positions based on keyboard input.
  - **Collision Detection**:Checks if the ball collides with the boss to deal damage.
  - **Event-driven Mechanics**: Actions like ability usage and movement are driven by player inputs (key presses) or random events (like the boss using abilities).

## Statistical Data
### Data Features
  - **Average Player Dash Usage**: Track dash usage per game
  - **Average Ability Usage**: Track ability usage per character
  - **Most Chosen Character by Player**: Track character selection
  - **Time Played**: Measures how long the player has been in each session
  - **Enemies Defeated**: Tracks the number of bosses defeated by the player.

### Data Recording Method
Data will be stored in a CSV file. Each row will contain metrics such as time played, enemies defeated

### Data Analysis Report
The data will be presented in tables for easy visualization.

| Feature | Why It's Good to Have | How to Obtain 50 Values | Class & Variable | How to Display |
|----------|----------|----------|----------|----------------|
| Average Player Dash Usage Per Boss | To balance dash ability and see player behavior.  | Track dash usage per game session for 50 sessions.  |Player class, dash_count | bar chart      |
| Average Ability Usage (Per Character)  | Helps with character and ability balance.  | Track ability usage per character over 50 sessions.   |Player class, ability_usage_count| bar chart      |
| Time Played Per Player | Understand engagement and game length preferences.  | Track total time played for 50 sessions.   |Player class, total_playtime| boxplot     |
|Enemies Defeated | Tracks how often the boss is defeated by player   | Tracks how often the boss is defeated by player in 50 games.   |Player class,boss_defeated | bar chart   |
|Most Chosen Character by Player | Understand player preferences for characters.  | Track character selection across 50 sessions.  |Player class, selected_character| pie chart   |

### Graph

|        | Feature | type      | x-axis | y-axis |
|--------|---------|-----------|-----|---|
| graph1 |Time Played| Boxplot   | -   | - |
| graph2 |Average Player Dash | Bar chart | Type of boss | Average dash used |
| graph3 |Average Ability Usage| Bar chart | Character Type | Average Ability Usage Count |
| graph4 |Enemies Defeated| Bar chart | Character Type | Boss defeat |
| graph5 | Most Chosen Character by Player| Pie chart | -   | - |

### Video

[Video link](https://youtu.be/O1eUmjmw_cQ)
