# Scior: Execution Modes

This document presents all Scior's arguments and their usage.

## Contents

  - [Arguments](#arguments)
    - [Groups of Arguments](#groups-of-arguments)
  - [Positional Arguments: Input Ontology File](#positional-arguments-input-ontology-file)
  - [Automation Level Modes (Optional Argument)](#automation-level-modes-optional-argument)
  - [World Assumption Modes (Optional Argument)](#world-assumption-modes-optional-argument)
  - [Verbosity (Optional Arguments)](#verbosity-optional-arguments)
  - [Output gUFO (Optional Arguments)](#output-gufo-optional-arguments)
  - [Software's Information: Help and Version](#softwares-information-help-and-version)

## Arguments

For executing Scior, the user should provide arguments related to the software's automation level and to the input model's completeness. The Scior's usage generated by the **help** argument is:

```txt
usage: scior [-h] [-i | -a] [-cwa | -owa | -owaf] [-s | -r | -d] [-gr | -gi | -gw] [-v] ontology_file
```

We are going to present each one of the arguments in the next sections.

### Groups of Arguments

We can divide the arguments into the following groups:

- Positional arguments
- Automation Level
- World Assumption
- Verbosity
- Output gUFO
- Software's Information

We present each one of these in the following sections. In all available groups, the asterisk in the argument description indicates that this is the default argument, i.e., the one that is adopted when the user does not declare an option.

## Positional Arguments: Input Ontology File

The only mandatory argument (positional argument) is the `ontology_file`, which is the path to the input ontology file. This file can be stored locally (i.e., offline in the user's file system) or remotely (i.e., online, web stored) and is the ontology that is going to have its semantics improved by Scior.

We implemented Scior using the [RDFLib Python library](https://rdflib.readthedocs.io/en/stable/), hence the software accepts rdf-based ontology files written in all its supported syntaxes. Once the syntax is valid, Scior automatically identifies and processes it. For consulting a table with all supported syntaxes, please refer to the [RDFLib parsing documentation page](https://rdflib.readthedocs.io/en/stable/intro_to_parsing.html).

## Automation Level Modes (Optional Argument)

Scior provides two execution modes regarding user's interactivity: totally automatic (i.e., no interaction is required at any moment) or interactive execution (when the user can provide information whenever necessary). The arguments for setting these execution modes are:

```txt
-i, --interactive    Execute automatic rules whenever possible, interactive rules when necessary.                
-a, --automatic      * Execute only automatic rules. Interactive rules are not performed.
```

As a premise, Scior always considers the number of possibilities to (positively or negatively) attribute a classification to a class: if the number of possibilities is one, no interaction is needed and hence it automatically attributes the classification to the class. If the number of possibilities is higher than one, Scior will require the user's interaction or report the situation to the user, when in the interactive and automatic modes, respectively. The information about actions considering different situations are presented [in the corresponding documentation](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Implemented-Rules-Actions.md).

## World Assumption Modes (Optional Argument)

Another piece of information that the user should provide to Scior is the completeness of the model to be evaluated. Scior considers this information for performing different actions according to its world assumption. The three available options are:

```txt
-cwa,   --is_cwa    Operate in Closed-World Assumption (CWA).
-owa,   --is_owa    * Operate in Open-World Assumption (OWA) – Regular Mode.
-owaf,  --is_owaf   Operate in Open-World Assumption (OWA) – Forced Mode.
```

RDF-based knowledge graphs are implemented over the [open-world assumption](https://en.wikipedia.org/wiki/Open-world_assumption) paradigm, where unknown information may be true or false—i.e., in this paradigm, it is supposed that the model may be **incomplete**. Pieces of information may be (intentionally or not) missing from the input file and the Scior engine must know that to infer each entity’s correct ontological categories. On one hand, the open-world assumption may cause Scior to identify more possibilities to be displayed to the user's choice when using the interactive mode, but it may also lead to fewer inferences when in the automatic mode.

Scior also provides a variation of the open-world assumption, the OWA-F (forced mode), that assumes that attributes a resulting value to a class whenever this class is identified as a single option to achieve the evaluated rule’s result.

When informing that the input model is complete, Scior performs in [closed-world assumption](https://en.wikipedia.org/wiki/Closed-world_assumption), where all unknown information is assumed to be false. The consequence of setting a model as complete is that Scior can perform more inferences, especially when in the automatic mode, as it can assume some information to be true, generating fewer possibilities. Operating in closed-world assumption also can lead Scior to generate inconsistencies (which cause the software to interrupt its execution) instead of incompleteness (which is only reported as a warning).

While some rules are performed the same way in both modes, others have different behaviors when the user sets different configurations. We present the different behavior of all rules regarding the automation level and regarding models' completeness in a [specific documentation](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Implemented-Rules-Actions.md).

## Verbosity (Optional Arguments)

The user can choose among printing only the necessary execution information, printing all generated information or do not print any information.

```txt
-s, --silent     Silent mode. Print only basic execution status information.
-r, --verbose    * Print basic execution information and results.
-d, --debug      Generates tons of log for debugging.
```

## Output gUFO (Optional Arguments)

The arguments of this group regard the output file generated after Scior’s execution is concluded, when it saves an output file containing all the discovered gUFO information (more information [here](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Functioning.md#output-ontology)).

```txt
-gr,  --gufo_results    * Write in the output ontology file only the gUFO classifications found.
-gi,  --gufo_import     Import gUFO ontology in the output ontology file.
-gw,  --gufo_write      Write all gUFO statements in the output ontology file.
```

By default, the output file only references the gUFO concepts in its assertions (so the only known gUFO information is the one that is contained in the file).

If the user wants to store or manipulate **gUFO** information in the output file, it can be done through the options `gi` and `gw`. The former uses the [`owl:imports` property](https://www.w3.org/TR/owl-ref/#imports-def) to reference and exhibit all gUFO in the output file. The latter argument merges the output file with gUFO, creating a unique ontology with all statements.

## Software's Information: Help and Version

The two last arguments are the ones to print a help message and the software version:

```txt
-h, --help      Show this help message and exit.
-v, --version   Print the software version and exit.
```

The **help** argument is a default functionality provided by the [Python argparse library](https://docs.python.org/3/library/argparse.html). When a user requests help, the software returns a string containing a help message, including the program usage and information about its available arguments. Finally, the **version** argument simply prints the version of Scior being executed.
