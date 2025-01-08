# Codebook for Social Value Orientation (SVO) Experiment

This codebook provides a detailed explanation of the variables, treatments, and computations used in the Social Value Orientation (SVO) experiment.

## Overview

The SVO experiment is based on the slider measure proposed by Murphy et al. (2011). Participants make choices from six matrices, each reflecting their preferences regarding the trade-off between their own payoffs and those of another participant. These choices are used to classify participants into one of four social preference categories:
- **Competitive**
- **Individualist**
- **Prosocial**
- **Altruist**

---

## Constants

| **Variable**         | **Type**   | **Description**                                                                                                   |
|-----------------------|------------|-------------------------------------------------------------------------------------------------------------------|
| `name_in_url`        | String     | Name of the app in the URL (`yssvo`).                                                                             |
| `players_per_group`  | Integer    | Number of players per group (2).                                                                                  |
| `num_rounds`         | Integer    | Number of rounds in the experiment (1).                                                                          |
| `matrices`           | Dictionary | Six matrices representing payoff scenarios for self and others (9 options per matrix).                           |
| `conversion_rate`    | Float      | Conversion rate from experimental points to real-world currency (default: 0.05).                                  |

### Matrices

Each matrix represents a unique payoff structure for the self and the paired participant. The matrices are:
1. **Matrix 1**: Fixed self-payoff (`85`), decreasing payoff for the other.
2. **Matrix 2**: Increasing payoffs for both self and the other.
3. **Matrix 3**: Increasing self-payoff, decreasing other-payoff.
4. **Matrix 4**: Sharply decreasing other-payoff while increasing self-payoff.
5. **Matrix 5**: Symmetric payoff changes around a midpoint of `75`.
6. **Matrix 6**: Both payoffs increase and converge to a fixed value (`85`).

---

## Subsession

| **Variable**           | **Type**   | **Description**                                                                            |
|-------------------------|------------|--------------------------------------------------------------------------------------------|
| `svo_conversion_rate`   | Float      | Conversion rate for the session (from session config or default).                          |

### Methods
- **`creating_session`**: Initializes the `svo_conversion_rate` for the session.
- **`vars_for_admin_report`**: Provides admin-level data, including matrices and participant-level choices and payoffs.

---

## Group

| **Variable**           | **Type**   | **Description**                                                                            |
|-------------------------|------------|--------------------------------------------------------------------------------------------|
| `svo_paid_choice`       | Integer    | Randomly selected matrix (1–6) used to compute participant payoffs.                        |

### Methods
- **`compute_payoffs`**: Randomly selects a matrix and computes payoffs for participants based on their choices.

---

## Player

| **Variable**           | **Type**       | **Description**                                                                            |
|-------------------------|----------------|--------------------------------------------------------------------------------------------|
| `svo_1` to `svo_6`      | Integer        | Participant's choice (0–8) for each matrix.                                                |
| `svo_payoff`            | Integer        | Payoff for the participant in points.                                                     |
| `svo_mean_self`         | Float          | Average payoff for self across all six matrices.                                          |
| `svo_mean_other`        | Float          | Average payoff for the other participant across all six matrices.                         |
| `svo_score`             | Float          | Social Value Orientation (SVO) score in degrees.                                          |
| `svo_classification`    | String         | Classification of the participant: `competitive`, `individualist`, `prosocial`, or `altruist`. |

### Methods
- **`compute_payoff`**:
  - Determines the payoff for the randomly selected matrix (`svo_paid_choice`).
  - Computes average payoffs (`svo_mean_self`, `svo_mean_other`) and SVO score.
  - Classifies the participant based on their SVO score.
- **`vars_for_template`**: Prepares the matrices for display in the participant interface.

---

## Key Computations

### Payoffs
- **Matrix Selection**: A random matrix (`svo_paid_choice`) is selected to determine payoffs.
- **Payoff Calculation**:
  - **If Player 1**: Payoff is determined by Player 1's choice from the selected matrix.
  - **If Player 2**: Payoff is determined by Player 1's choice, which applies to both participants.

### SVO Score
- Calculated as:
  $
  \text{SVO Score} = \arctan\left(\frac{\text{svo_mean_other} - 50}{\text{svo_mean_self} - 50}\right)
  $
  - The result is converted from radians to degrees.

### Classification
- **Competitive**: $\text{SVO Score} \leq -12.04 $
- **Individualist**: $ -12.04 < \text{SVO Score} \leq 22.45 $
- **Prosocial**: $ 22.45 < \text{SVO Score} \leq 57.15 $
- **Altruist**: $ \text{SVO Score} > 57.15 $

---

## Participant Interface

Participants are presented with six matrices, each containing nine options. They select one option per matrix, reflecting their preferences for self and other payoffs.

At the end of the session:
- A randomly selected matrix determines the final payoff.
- Participants are informed of their payoffs and SVO classification.

---

## Admin Report

The admin report includes:
1. **Matrix Data**: The payoff options for each matrix.
2. **Participant Information**:
   - Group and individual choices.
   - Payoffs and classifications.


