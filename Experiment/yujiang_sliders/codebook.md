# Codebook for Slider Task Experiment

This codebook provides a detailed explanation of the variables, mechanics, and computations used in the slider task experiment.

---

## Overview

The slider task is a simple effort-based experiment where participants adjust sliders to match predefined target values. The experiment consists of two rounds, and participants' payoffs depend on their total performance across both rounds.

---

## Constants

| **Variable**       | **Type**   | **Description**                                                                                   |
|---------------------|------------|---------------------------------------------------------------------------------------------------|
| `name_in_url`      | String     | Name of the app in the URL (`yss`).                                                               |
| `players_per_group`| NoneType   | No grouping is applied; all players are in individual sessions.                                   |
| `num_rounds`       | Integer    | Number of rounds in the experiment (2).                                                          |
| `flat_rate`        | Currency   | Payment received if the performance requirement is met (`10 units`).                             |
| `show_up_fee`      | Currency   | Payment received if the performance requirement is not met (`2 units`).                          |
| `requirement`      | Integer    | Minimum total number of correct sliders needed to qualify for the flat rate (15).                |
| `time_given`       | Integer    | Time allocated for each round (`420 seconds`).                                                   |

---

## Subsession

| **Variable**           | **Type**   | **Description**                                                                                 |
|-------------------------|------------|-------------------------------------------------------------------------------------------------|
| `vars_for_admin_report` | Method     | Prepares admin-level data, including participant scores, total scores, and payoffs.             |

### Methods
- **`creating_session`**:
  - Generates 10 random slider target values for each player in both rounds.
  - Stores these values in the `participant.vars` dictionary.

- **`vars_for_admin_report`**:
  - Compiles a summary report of all participants, including:
    - Total sliders correctly adjusted.
    - Whether they qualify to continue the experiment based on the performance requirement.
    - Final payoffs.

---

## Group

This experiment does not utilize grouping, so the `Group` class is unused.

---

## Player

| **Variable**             | **Type**       | **Description**                                                                               |
|---------------------------|----------------|---------------------------------------------------------------------------------------------|
| `slider1` to `slider10`   | Integer        | Current values of the 10 sliders, initialized to `0`.                                        |
| `total_sliders_correct`   | Integer        | Total number of sliders correctly adjusted in the current round.                            |

### Methods
- **`check_slider_answers`**:
  - Compares the player's slider values to the target values for the current round.
  - Updates the `total_sliders_correct` field for the round.
  - Computes the cumulative score across all rounds and assigns a payoff:
    - **Flat Rate**: Awarded if the total score meets or exceeds the `requirement`.
    - **Show-Up Fee**: Awarded if the total score is below the `requirement`.
  - Stores the payoff and summary message in `participant.vars`.

---

## Payoff Structure

### Criteria
1. **Flat Rate**:
   - Awarded if the total number of correctly adjusted sliders across both rounds is **15 or more**.
   - Payment: `10 units`.

2. **Show-Up Fee**:
   - Awarded if the total number of correctly adjusted sliders is **less than 15**.
   - Payment: `2 units`.

---

## Participant Interface

### Task
- Participants see 10 sliders, each with a range of `0–100`.
- They adjust the sliders to match randomly generated target values.

### Feedback
- After each round, participants see how many sliders they adjusted correctly.
- At the end of the second round, participants receive:
  - Their total number of correct sliders across both rounds.
  - Their final payoff.

---

## Admin Report

The admin report provides:
1. **Participant-Level Data**:
   - Player ID.
   - Total sliders correctly adjusted.
   - Total score across all rounds.
   - Payoff.
   - Whether they met the performance requirement.

2. **Summary**:
   - Allows experimenters to quickly evaluate participant performance and payoffs.

---

## Summary

This slider task experiment evaluates participants' effort and precision by requiring them to match slider values to predefined targets. It incorporates a clear performance-based payoff structure and provides both participants and experimenters with detailed feedback.
