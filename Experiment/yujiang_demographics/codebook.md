# Codebook for Demographic Questionnaire (YSDEM)

This document provides an overview of the variables and logic in the **Demographic Questionnaire** app. The app collects key demographic and socio-economic information from participants to contextualize their responses and behaviors in the experiment.

---

## Overview

The **Demographic Questionnaire** collects the following types of data:
1. Personal information (e.g., year of birth, gender, nationality).
2. Education background and socio-professional details.
3. Political orientation and past experiment participation.

---

## Constants

| **Variable**     | **Type** | **Description**                                                                 |
|-------------------|----------|---------------------------------------------------------------------------------|
| `name_in_url`    | String   | Name of the app in the URL (`ysdem`).                                           |
| `players_per_group` | None     | No grouping; all players are treated individually.                             |
| `num_rounds`     | Integer  | Number of rounds (1).                                                           |
| `disciplines`    | List     | List of study disciplines for participant selection.                            |
| `revenus`        | List     | List of income categories for participant self-reporting.                       |

---

## Subsession Variables

| **Variable**  | **Type** | **Description**                                                                 |
|---------------|----------|---------------------------------------------------------------------------------|
| None          |          | No specific subsession-level variables are defined.                            |

---

## Group Variables

| **Variable**  | **Type** | **Description**                                                                 |
|---------------|----------|---------------------------------------------------------------------------------|
| None          |          | No specific group-level variables are defined.                                 |

---

## Player Variables

### Personal Information

| **Variable**      | **Type**       | **Description**                                                                 |
|--------------------|----------------|---------------------------------------------------------------------------------|
| `year_of_birth`   | IntegerField   | Participant's year of birth. Choices range from the current year - 15 to the current year - 101. |
| `gender`          | IntegerField   | Participant's gender. Choices: 0 = Female, 1 = Male.                           |
| `nationality`     | StringField    | Participant's nationality. Uses predefined country codes.                      |
| `marital_status`  | IntegerField   | Participant's marital status. Choices: Single, Pacsé(e), Married, Divorced, Widowed. |

### Education and Profession

| **Variable**             | **Type**       | **Description**                                                                 |
|---------------------------|----------------|---------------------------------------------------------------------------------|
| `student`               | BooleanField   | Indicates if the participant is currently a student.                           |
| `study_level`           | IntegerField   | Participant's level of education. Choices range from "Bac" to "Bac+8".         |
| `study_discipline`      | IntegerField   | Participant's discipline of study. Uses a predefined list of disciplines.       |
| `socioprofessional_group` | IntegerField   | Socio-professional category. Choices include various occupational groups.       |

### Political Orientation

| **Variable**      | **Type**       | **Description**                                                                 |
|--------------------|----------------|---------------------------------------------------------------------------------|
| `politique`       | IntegerField   | Participant's political orientation on a scale from 0 (left) to 10 (right).     |

### Experiment Experience

| **Variable**                  | **Type**       | **Description**                                                                 |
|--------------------------------|----------------|---------------------------------------------------------------------------------|
| `experiment_participation`    | BooleanField   | Indicates if the participant has ever participated in an economic experiment.  |

---

## Notes

- The app supports multilingual labels using Django's translation framework, allowing customization based on participant language preferences.
- The questionnaire includes both mandatory (e.g., nationality) and optional fields (e.g., socio-professional group).
- The political orientation question uses a labeled numeric scale to assess participants' self-placement on the political spectrum.
