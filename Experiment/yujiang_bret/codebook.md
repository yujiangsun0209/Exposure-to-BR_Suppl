# Codebook for Bomb Risk Elicitation Task (BRET)

This document provides an overview of the variables and logic in the **Bomb Risk Elicitation Task (BRET)** app. The app evaluates participants' risk preferences by asking them to decide how many boxes to collect, with one box containing a bomb that would nullify their earnings for the task.

---

## Overview

- **Objective**: Assess risk-taking behavior under uncertainty.
- **Game Rules**:
  - Participants decide how many boxes to collect.
  - One box randomly contains a "bomb."
  - If the bomb is in the collected boxes, all earnings for the task are forfeited. Otherwise, participants earn a fixed amount per collected box.

---

## Constants

| **Variable**      | **Type**  | **Description**                                                                 |
|--------------------|-----------|---------------------------------------------------------------------------------|
| `name_in_url`     | String    | Name of the app in the URL (`ysb`).                                             |
| `players_per_group` | None     | No grouping; all players are treated individually.                             |
| `num_rounds`      | Integer   | Number of rounds (1).                                                           |
| `num_rows`        | Integer   | Number of rows in the grid (10).                                                |
| `num_cols`        | Integer   | Number of columns in the grid (10).                                             |
| `num_boxes`       | Integer   | Total number of boxes in the grid (`num_rows * num_cols`, i.e., 100).           |
| `box_height`      | String    | Height of each box in pixels (`30px`).                                          |
| `box_width`       | String    | Width of each box in pixels (`30px`).                                           |
| `random_payoff`   | Boolean   | Whether the payoff is randomly determined (`False`).                            |
| `feedback`        | Boolean   | Whether feedback is provided (`True`).                                          |
| `results`         | Boolean   | Whether results are displayed to participants (`True`).                         |
| `dynamic`         | Boolean   | Whether the game uses dynamic updates (`False`).                                |
| `time_interval`   | Float     | Time interval for dynamic updates (`1.00`).                                     |
| `random`          | Boolean   | Whether the bomb's position is randomized (`True`).                             |
| `devils_game`     | Boolean   | Whether the game includes additional challenges (`False`).                      |
| `undoable`        | Boolean   | Whether collected boxes can be undone (`False`).                                |

---

## Subsession Variables

| **Variable**      | **Type**       | **Description**                                                                 |
|--------------------|----------------|---------------------------------------------------------------------------------|
| `box_value`       | FloatField     | The monetary value of each collected box. Defaults to 0.1 (configured via session). |

---

## Group Variables

| **Variable**  | **Type** | **Description**                                                                 |
|---------------|----------|---------------------------------------------------------------------------------|
| None          |          | No specific group-level variables are defined.                                 |

---

## Player Variables

| **Variable**          | **Type**       | **Description**                                                                 |
|------------------------|----------------|---------------------------------------------------------------------------------|
| `bomb`               | IntegerField   | Indicates if the bomb was in the collected boxes (`1` if true, `0` otherwise).  |
| `bomb_row`           | PositiveIntegerField | The row number where the bomb is located.                                      |
| `bomb_col`           | PositiveIntegerField | The column number where the bomb is located.                                   |
| `boxes_collected`    | IntegerField   | The number of boxes collected by the participant.                               |
| `payoff`             | CurrencyField  | The calculated payoff based on collected boxes and bomb outcome.               |

---

## Methods

### Subsession

| **Method**           | **Description**                                                                 |
|-----------------------|---------------------------------------------------------------------------------|
| `creating_session`   | Sets the monetary value for each collected box based on session configuration.  |
| `vars_for_admin_report` | Collects and formats data for the admin report.                               |

### Player

| **Method**           | **Description**                                                                 |
|-----------------------|---------------------------------------------------------------------------------|
| `set_payoff`         | Calculates the player's payoff based on collected boxes and bomb presence.      |
| `vars_for_template`  | Provides variables for rendering the game interface (e.g., grid dimensions).    |

---

## Notes

- **Bomb Placement**: The bomb is randomly assigned to one box in the grid.
- **Feedback**: Players are informed of the bomb's location and whether their collected boxes included the bomb.
- **Payoff Rules**:
  - If the bomb is collected, the payoff is `0`.
  - Otherwise, the payoff is calculated as `boxes_collected * box_value`.
- **Participant Variables**:
  - `yujiang_bret_payoff`: Stores the payoff from the task.
  - `yujiang_bret_txt_final`: Provides a detailed explanation of the player's result in the task.

--- 

## Admin Report

The admin report includes:
- Player ID (`joueur`).
- Participant label (`label`).
- Total payoff for the task (`payoff`).
