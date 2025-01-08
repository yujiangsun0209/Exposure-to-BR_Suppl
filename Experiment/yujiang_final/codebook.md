# Codebook for Final Screen (YSFIN)

This document details the variables and logic used in the **final screen** of the experiment. This screen consolidates participant payoffs from different parts of the experiment and collects additional comments.

---

## Overview

The **final screen** serves as a summary and reporting stage for participants. It performs the following functions:
1. Randomly selects one of two tasks from Part 2 for final payoff computation.
2. Combines payoffs from Part 1 and the selected task in Part 2.
3. Optionally collects participant comments.

---

## Constants

| **Variable**         | **Type** | **Description**                        |
|-----------------------|----------|----------------------------------------|
| `name_in_url`        | String   | Name of the app in the URL (`ysfin`).  |
| `players_per_group`  | None     | No grouping; all players are treated individually. |
| `num_rounds`         | Integer  | Number of rounds (1).                  |

---

## Subsession Variables

| **Variable**  | **Type** | **Description**                                                                 |
|---------------|----------|---------------------------------------------------------------------------------|
| `vars_for_admin_report` | Function | Collects participant information for administrative reporting.         |

The `vars_for_admin_report` function collects and reports the following data for each participant:
- `joueur`: Player ID.
- `label`: Participant label.
- `part1_payoff`: Payoff from Part 1 (`yujiang_main_payoff`).
- `part2_selected_task`: The selected task from Part 2 for payoff computation.
- `part2_payoff`: Payoff from the selected task in Part 2.
- `payoff`: Final payoff, combining Part 1 and Part 2.

---

## Group Variables

No group-level variables are used in this app.

---

## Player Variables

| **Variable**          | **Type**         | **Description**                                                                                  |
|------------------------|------------------|--------------------------------------------------------------------------------------------------|
| `part2_selected_task` | IntegerField     | Randomly selected task from Part 2 for payoff computation (1 or 2).                             |
| `comments`            | LongStringField  | Optional participant comments, collected as free-form text.                                     |

---

## Payoff Computation Logic

The `start` method handles the computation of final payoffs:

1. **Part 1 Payoff:**
   - Retrieved from `yujiang_main_payoff` stored in the participant's variables.

2. **Part 2 Task Selection:**
   - A task is randomly selected (1 or 2):
     - **Task 1:** Uses `yujiang_bret_payoff` from Part 2.
     - **Task 2:** Uses `yujiang_svo_payoff` from Part 2.

3. **Final Payoff:**
   - The payoff from Part 1 is combined with the payoff from the selected Part 2 task.
   - The result is assigned to the participant's `payoff` variable.

4. **Participant Payoff Storage:**
   - The computed final payoff is stored in the `participant.payoff` variable.

---

## Notes

- This app primarily serves as a summarization tool, consolidating payoffs from prior parts of the experiment.
- The random selection of a task in Part 2 ensures variability and incentivizes attention in both tasks.
- Participants can optionally leave comments, providing feedback or other insights at the end of the experiment.
