# Codebook for Allocation Choice Experiment (YSM)

This document provides detailed information about the variables and constructs in the allocation choice experiment. This experiment involves allocating an endowment in different treatment conditions.

---

## Overview

The experiment investigates decision-making behavior in allocation tasks under various treatment conditions:
- **Baseline (0):** Standard allocation task.
- **One-Sided Dictator (1):** Only the dictator is subject to a background risk.
- **One-Sided Recipient (2):** Only the recipient is subject to a background risk.
- **Common Symmetric (3):** Both players are subject to the same background risk.
- **Common Independent (4):** Both players are subject to independent background risks.

Participants interact in pairs as either a **dictator** or a **recipient**.

---

## Constants

| **Variable**         | **Type** | **Description**                                                                                   |
|-----------------------|----------|---------------------------------------------------------------------------------------------------|
| `name_in_url`        | String   | Name of the app in the URL (`ysm`).                                                               |
| `players_per_group`  | Integer  | Number of players per group (2).                                                                  |
| `num_rounds`         | Integer  | Number of rounds in the experiment (1).                                                          |
| `endowment`          | Currency | Amount given to the dictator to allocate (`€20`).                                                |
| `magnitude_BR`       | Currency | Magnitude of the background risk (`€10`).                                                        |
| `flat_rate`          | Currency | Initial flat rate given to both participants to ensure minimum ability to afford potential loss. |
| `baseline`           | Integer  | Treatment ID for the baseline condition (`0`).                                                   |
| `one_sided_dictator` | Integer  | Treatment ID for the one-sided dictator condition (`1`).                                         |
| `one_sided_recipient`| Integer  | Treatment ID for the one-sided recipient condition (`2`).                                        |
| `common_sym`         | Integer  | Treatment ID for the common symmetric condition (`3`).                                           |
| `common_indep`       | Integer  | Treatment ID for the common independent condition (`4`).                                         |

---

## Subsession Variables

| **Variable**  | **Type** | **Description**                                                                 |
|---------------|----------|---------------------------------------------------------------------------------|
| `treatment`  | Integer  | Current treatment condition, defined in session configuration.                 |

---

## Group Variables

| **Variable** | **Type**     | **Description**                                                                                     |
|--------------|--------------|-----------------------------------------------------------------------------------------------------|
| `give`      | CurrencyField| Amount sent by the dictator to the recipient.                                                      |
| `die_1`     | IntegerField | Result of the first die roll, affecting dictator's payoff in certain treatments.                   |
| `die_2`     | IntegerField | Result of the second die roll, affecting recipient's payoff in the **common independent** treatment.|

---

## Player Variables

| **Variable**      | **Type**         | **Description**                                                                                 |
|--------------------|------------------|-------------------------------------------------------------------------------------------------|
| `attempt_1`       | IntegerField     | Response to the first attention check question.                                                |
| `attempt_2`       | IntegerField     | Response to the second attention check question.                                               |
| `attempt_3`       | IntegerField     | Response to the third attention check question.                                                |
| `ans_check`       | IntegerField     | Count of incorrect answers in the attention check.                                             |
| `gachter_circles` | IntegerField     | Participant's choice in the Gächter circles task (additional task unrelated to treatments).    |

---

## Treatments

1. **Baseline (0):**
   - Payoffs are determined solely by the dictator's allocation (`give`).
   - No additional risks are introduced.

2. **One-Sided Dictator (1):**
   - The dictator's payoff is affected by a background risk (`die_1`).

3. **One-Sided Recipient (2):**
   - The recipient's payoff is affected by a background risk (`die_1`).

4. **Common Symmetric (3):**
   - Both players are subject to the same background risk (`die_1`).

5. **Common Independent (4):**
   - Both players are subject to independent background risks (`die_1` for dictator, `die_2` for recipient).

---

## Attention Check

Three attention check questions are presented to participants. The correct answers depend on the treatment condition:
- Treatment-specific logic evaluates the correctness of responses.
- Incorrect answers are tracked using the `ans_check` variable.

---

## Payoff Calculation

Payoffs are calculated based on the treatment:
- **Baseline:** Payoffs depend solely on the dictator's allocation.
- **Other Treatments:** Payoffs incorporate background risk, which is influenced by the results of die rolls.

The **background risk** modifies payoffs:
- A die roll of **odd** decreases the payoff by `€10`.
- A die roll of **even** increases the payoff by `€10`.

---

## Final Summary

The `set_txt_final` function generates a textual explanation of the payoffs for each player based on their decisions, roles, and the treatment condition. This summary is stored in the participant's variables for reporting purposes.

---

## Notes

- All participants receive a **flat rate (€10)** at the start to ensure they can absorb potential losses from background risk.
- **Attention Check Questions:** The responses and logic vary based on the treatment and aim to ensure participant comprehension.
- **Die Rolls:** The randomness introduced by die rolls simulates background risk and varies across treatments.
