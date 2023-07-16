# Scior: Implemented Rules Actions

Scior’s rules that are existentially quantified need decision taking actions, which must be done automatically by it or interactively by the user. This applies to the rules from the groups [UFO Some](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Implemented-Rules-Definitions.md#ufo-some-rules-group) and [UFO Unique](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Implemented-Rules-Definitions.md#ufo-unique-rules-group).

The interactive operation mode is unavailable in the current version of Scior. When this functionality returns, the actions for this mode will be included in this document.

It is essential to keep in mind that Scior has the following considerations:

- Scior assumes that all classes are different from each other in all its operation modes.

- Scior only assigns positive or negative classifications to classes. It does not assign equality or difference classifications between classes.

## Action Calculation

For the rule being evaluated, the action to be taken depends on the number of elements already classified and on the number of elements that have no restrictions to receive the intended classification (i.e., that candidates to receive the intended classification). Hence, Scior creates two lists:

- `is_list`: list of classes identified as already being of the desired classification.

- `can_list`: list of classes identified as candidates for being of the desired classification.

The actions to be taken depend on the number of elements in each of these lists. Examples are provided in the image below.

![example calc](https://raw.githubusercontent.com/unibz-core/Scior/main/documentation/resources/images/lists_calculation.png)

## Actions

A complete table with all actions compiled is available in `.tsv` (tab-separated) format and can be [ACCESSED HERE](https://github.com/unibz-core/Scior/blob/main/documentation/resources/scior_actions.tsv). Both in this document and in the `.tsv` file, the number 2 in the tables represents *two or more* possibilities.

### Possible Actions

- No action.

- Report incompleteness and no possibility.

- Report incompleteness and possibilities (OR - multiple options can be chosen).

- Report incompleteness and possibilities (XOR - a single option can be chosen).

- Report incompleteness and single possibility (only a single option is available).

- Report inconsistency.

- Set all classes in `can_list` (for the operation being evaluated) as **not type**.

- Set class in `can_list` (for the operation being evaluated) as **type**.

### Actions for World Assumption and Rule Group

#### OWA – Some

| **Length IS_LIST** | **Length CAN_LIST** | **Automatic action**                          |
|--------------------|---------------------|-----------------------------------------------|
| 0                  | 0                   | Report incompleteness and no possibility.     |
| 0                  | 1                   | Report incompleteness and single possibility. |
| 0                  | 2                   | Report incompleteness and possibilities (OR). |
| 1                  | 0                   | No action.                                    |
| 1                  | 1                   | No action.                                    |
| 1                  | 2                   | No action.                                    |
| 2                  | 0                   | No action.                                    |
| 2                  | 1                   | No action.                                    |
| 2                  | 2                   | No action.                                    |

#### OWA – Unique

| **Length IS_LIST** | **Length CAN_LIST** | **Automatic action**                           |
|--------------------|---------------------|------------------------------------------------|
| 0                  | 0                   | Report incompleteness and no possibility.      |
| 0                  | 1                   | Report incompleteness and single possibility.  |
| 0                  | 2                   | Report incompleteness and possibilities (XOR). |
| 1                  | 0                   | No action.                                     |
| 1                  | 1                   | Set all classes in can list as not type.       |
| 1                  | 2                   | Set all classes in can list as not type.       |
| 2                  | 0                   | Report inconsistency.                          |
| 2                  | 1                   | Report inconsistency.                          |
| 2                  | 2                   | Report inconsistency.                          |

#### OWA-F – Some

| **IS** | **Length CAN_LIST** | **Automatic Action**                          |
|--------|---------------------|-----------------------------------------------|
| 0      | 0                   | Report incompleteness and no possibility.     |
| 0      | 1                   | Set class in can list as type.                |
| 0      | 2                   | Report incompleteness and possibilities (OR). |
| 1      | 0                   | No action.                                    |
| 1      | 1                   | No action.                                    |
| 1      | 2                   | No action.                                    |
| 2      | 0                   | No action.                                    |
| 2      | 1                   | No action.                                    |
| 2      | 2                   | No action.                                    |

#### OWA-F – Unique

| **Length IS_LIST** | **Length CAN_LIST** | **Automatic Action**                           |
|--------------------|---------------------|------------------------------------------------|
| 0                  | 0                   | Report incompleteness and no possibility.      |
| 0                  | 1                   | Set class in can list as type.                 |
| 0                  | 2                   | Report incompleteness and possibilities (XOR). |
| 1                  | 0                   | No action.                                     |
| 1                  | 1                   | Set all classes in can list as not type.       |
| 1                  | 2                   | Set all classes in can list as not type.       |
| 2                  | 0                   | Report inconsistency.                          |
| 2                  | 1                   | Report inconsistency.                          |
| 2                  | 2                   | Report inconsistency.                          |

#### CWA – Some

| **Length IS_LIST** | **Length CAN_LIST** | **Automatic Action**                          |
|--------------------|---------------------|-----------------------------------------------|
| 0                  | 0                   | Report inconsistency.                         |
| 0                  | 1                   | Set class in can list as type.                |
| 0                  | 2                   | Report incompleteness and possibilities (OR). |
| 1                  | 0                   | No action.                                    |
| 1                  | 1                   | No action.                                    |
| 1                  | 2                   | No action.                                    |
| 2                  | 0                   | No action.                                    |
| 2                  | 1                   | No action.                                    |
| 2                  | 2                   | No action.                                    |

#### CWA – Unique

| **Length IS_LIST** | **Length CAN_LIST** | **Automatic Action**                           |
|--------------------|---------------------|------------------------------------------------|
| 0                  | 0                   | Report inconsistency.                          |
| 0                  | 1                   | Set class in can list as type.                 |
| 0                  | 2                   | Report incompleteness and possibilities (XOR). |
| 1                  | 0                   | No action.                                     |
| 1                  | 1                   | Set all classes in can list as not type.       |
| 1                  | 2                   | Set all classes in can list as not type.       |
| 2                  | 0                   | Report inconsistency.                          |
| 2                  | 1                   | Report inconsistency.                          |
| 2                  | 2                   | Report inconsistency.                          |
