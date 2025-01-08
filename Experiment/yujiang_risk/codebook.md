# Codebook for Risk and Trust Sensitivity Experiment

This codebook provides a detailed explanation of the variables and constructs used in the risk sensitivity and trust experiment, based on Dohmen et al. (2011).

---

## Overview

The experiment measures participants' self-reported:
- General risk sensitivity.
- Risk sensitivity in specific domains (health and financial matters).
- Patience level.
- Trust in others, both generally and in specific contexts.

Participants respond to questions on a Likert scale, where higher values indicate greater willingness to take risks, higher patience, or greater trust, depending on the context.

---

## Constants

| **Variable**       | **Type**   | **Description**                                         |
|---------------------|------------|-------------------------------------------------------|
| `name_in_url`      | String     | Name of the app in the URL (`ysri`).                   |
| `players_per_group`| NoneType   | No grouping is applied; all players are individual.    |
| `num_rounds`       | Integer    | Number of rounds in the experiment (1).               |

---

## Player Variables

| **Variable**                 | **Type**     | **Choices**                                                                                                  | **Description**                                                                 |
|-------------------------------|--------------|--------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| `risque_general`             | Integer      | 0–10, with 0 = "Not at all willing to take risks" and 10 = "Very willing to take risks".                     | Self-reported general willingness to take risks.                              |
| `risque_sante`               | Integer      | 0–10, same as above.                                                                                        | Self-reported willingness to take risks in health-related matters.            |
| `risque_argent`              | Integer      | 0–10, same as above.                                                                                        | Self-reported willingness to take risks in financial matters.                 |
| `patience`                   | Integer      | 0–10, with 0 = "Very impatient" and 10 = "Very patient".                                                    | Self-reported level of patience.                                              |
| `confiance_autres`           | Integer      | 0 = "One can never be too cautious", 1 = "Most people can be trusted".                                       | Binary response indicating general trust in others.                           |
| `confiance_autres_general`   | Integer      | 0–10, with 0 = "Very cautious in relationships with others" and 10 = "Very trusting in relationships".       | General trust in others, measured on a 0–10 scale.                            |
| `confiance_autres_famille`   | Integer      | 0–10, same as above.                                                                                        | Trust in family members, measured on a 0–10 scale.                            |
| `confiance_autres_travail`   | Integer      | 0–10, same as above.                                                                                        | Trust in colleagues or people in the workplace, measured on a 0–10 scale.     |

---

## Question Design

1. **Risk Sensitivity**:
   - Three questions assess willingness to take risks:
     - General.
     - In health matters.
     - In financial matters.
   - Responses are on a 0–10 Likert scale, where higher values indicate greater risk tolerance.

2. **Patience**:
   - Participants rate their patience on a 0–10 Likert scale, with higher values indicating greater patience.

3. **Trust**:
   - Participants respond to trust-related questions across four contexts:
     - Binary trust question about general attitudes toward others.
     - General trust in relationships (0–10).
     - Trust in family (0–10).
     - Trust in the workplace (0–10).

---

## Notes

- **Scales**:
  - For all 0–10 Likert scales, participants are presented with descriptive anchors at both ends to clarify the meaning of extreme values.

- **Data Usage**:
  - Responses can be analyzed to identify patterns in risk-taking, patience, and trust across different domains and contexts.
  - Cross-domain comparisons (e.g., trust vs. risk sensitivity) can provide insights into behavioral tendencies.

- **Binary Trust Question**:
  - The binary question on general trust is a simplified indicator and complements the more granular trust scales.

