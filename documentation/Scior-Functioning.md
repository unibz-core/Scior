# Scior: Functioning Overview

This document’s aim is to present an overview of Scior, also describing its structure and functioning mechanism. Besides the objectives and scope of Scior, we present in this document information regarding the execution and functioning of the software divided into three sections: input, execution, and output.

Please refer to this repository’s main [documentation file](https://github.com/unibz-core/Scior#readme) for instructions about the installation or execution of Scior.

## Content

- [Introduction](#introduction)
  - [Scope](#scope)
  - [Development Premises](#development-premises)
- [Input and Configurations](#input-and-configurations)
  - [Input File](#input-file)
  - [Arguments and Configurations](#arguments-and-configurations)
- [Data Initialization](#data-initialization)
  - [RDF Graphs](#rdf-graphs)
  - [Working Data Structure](#working-data-structure)
  - [Classifications’ Manipulation](#classifications-manipulation)
  - [Inferencing Method](#inferencing-method)
  - [Consistency Evaluations](#consistency-evaluations)
- [Rules Executions](#rules-executions)
  - [Rule Types](#rule-types)
  - [Hashing](#hashing)
  - [Execution Logic](#execution-logic)
  - [Information and Data Reporting](#information-and-data-reporting)
    - [User Interaction](#user-interaction)
    - [Reporting Information](#reporting-information)
    - [Reporting Incompleteness](#reporting-incompleteness)
    - [Reporting Inconsistencies](#reporting-inconsistencies)
- [Output Files](#output-files)
  - [Output Ontology](#output-ontology)
  - [Report File](#report-file)
- [Execution Statistics](#execution-statistics)

## Introduction

The quality of an information system directly depends on how truthful its information structures are and that we can only achieve such truthfulness with the support of highly expressive ontologies [[ref](https://direct.mit.edu/dint/article/2/1-2/181/10008)]. Contrary to reference ontologies, which are build with ontologically well-founded languages and that aim to provide such high expressiveness, lightweight ontologies like OWL knowledge graphs are not focused on representation adequacy but are designed with the focus on guaranteeing desirable computational properties, such as computational tractability and decidability [[ref](https://dl.acm.org/doi/abs/10.5555/1565421.1565425)].

We propose Scior to increase the semantics of OWL ontologies by classifying their represented domain concepts into foundational ontology concepts–to be more specific, into [gUFO](https://nemo-ufes.github.io/gufo/) ontological categories. Considering that gUFO is “a lightweight implementation of the [Unified Foundational Ontology (UFO)](https://nemo.inf.ufes.br/wp-content/uploads/ufo_unified_foundational_ontology_2021.pdf) *suitable for Semantic Web OWL 2 DL applications*”, Scior can rely on almost two decades of development of UFO to achieve its objectives.

### Scope

In its website, gUFO states that one of its key features is that “*it includes two taxonomies: one with classes whose instances are individuals (…) and another with classes whose instances are types (…)*”. The current version of Scior is limited to a subset of the second hierarchy, the hierarchy of types, as it handles only Endurant Types. I.e., Scior can classify OWL classes into subclasses of the `gufo:EndurantType` class.

The authors of gUFO document that its usage form is “*by specializing and instantiating its elements. Reuse of gUFO consists in instantiating and/or specializing the various classes, object properties and data properties defined in the ontology, inheriting from it the domain-independent distinctions of UFO*”. As dealing only with the hierarchy of types, all classifications performed by Scior are formalized with a `rdf:type` property between the domain class and its identified gUFO type. This strategy is aligned gUFO’s strategy to employ “*OWL 2 punning, when a class is also treated as an instance of another class (in this case, :Person rdf:type gufo:Kind and, as defined in gUFO, gufo:Kind rdf:type owl:Class)*”. Considering the use of RDF’s instantiation property only, the current implementation of Scior does not address multi-level modeling.

By deciding that the first release of Scior will comprise only Endurant Types, we are addressing two ontological meta-properties of entities: [sortality](https://ontouml.readthedocs.io/en/latest/theory/identity.html) (related to the *identity principle* the entity may provide or carry) and [rigidity](https://ontouml.readthedocs.io/en/latest/theory/rigidity.html), excluding only a third meta-property that is directly associated to the hierarchy of individuals, the *ontological nature*.

The published version of Scior already contains code for a future classification of classes considering the gUFO hierarchy of individuals. However, as this feature is currently out of scope, the related pieces of code are inactive and will be omitted in this document.

Another scope limitation is that Scior does not handle ontology entities different from `owl:Class`, `rdfs:subClassOf`, and `rdf:type`. I.e., only taxonomical relations are considered. Scior does not consider other properties as object properties and data properties in its current version. However, restricting the number of allowed ontology entities has the benefit of reducing the software’s execution time.

It must be made clear that the software is highly useful. Present how many percent of the classes in the catalog are of endurant types.

Finally, it is important to register that we aim to evolve the software’s scope is future versions, especially regarding the inclusion of (i) the identification of the ontological nature of entities (i.e., gUFO’s hierarchy of individuals), (ii) `gufo:EventType` and `gufo:SituationType`, (iii) properties different from taxonomical relations (e.g., relational properties, relations, and attributes), and (iv) multi-level modeling.

### Development Premises

To define a clear scope for Scior, we defined premises that guided the software development:

1. Scior cannot create new classes during its execution.
2. Scior cannot reclassify classes. I.e., the software can only set types still not (positively or negatively) attributed to a class.
3. Interaction can only be available when more than one option is available. Every time that there is a single classification option, Scior will automatically assert it.

## Input and Configurations

### Input File

The input ontology file is the only [mandatory input](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Execution-Modes.md) for Scior. This file must contain an rdf-based model, which is the ontology to be semantically improved during the software’s execution.

At the current version of Scior, the input file must have at least one class with a gUFO classification so that the software can infer another knowledge from it. I.e., if a user provides as input an ontology with no statement relating one of the ontology’s classes with a gUFO endurant type classification via a `rdf:type` property, the software will not perform any inference and, hence, it will generate the same ontology used in the input as output.

As stated in the previous section, the Scior performs its inferences reasoning over (the existence or absence of) specialization and instantiation properties (`rdfs:subClassOf` and `rdf:type`, respectively), consequently Scior is more likely to infer new knowledge in input models with large taxonomies than in input models with isolated classes.

You can find information about the input file location and accepted syntaxes in the [specific documentation](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Execution-Modes.md#input-ontology-file) about the software’s arguments.

### Arguments and Configurations

Please refer to the [respective documentation](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Execution-Modes.md) for detailed information about the Scior’s arguments and configurations.

## Data Initialization

### RDF Graphs

Scior uses three graphs that receive the following names: original graph, working graph, and gUFO graph.

The **original graph** is the complete input ontology loaded into an RDF Graph using the [RDFLib parse](https://rdflib.readthedocs.io/en/stable/intro_to_parsing.html) function. Scior keeps the original graph in memory because, by the end of its execution, this graph is going to be added with the identified gUFO classifications to be saved as the execution’s output.

Scior, however, has a [limited scope](#scope) and it does not need all the information contained in the original graph for its execution. Using the software over all the RDF statements in the original graph would be more time and resource costly than reducing the graph to another one that contains only the necessary information to perform Scior. Hence, Scior creates a second graph and names it **working graph**.

The working graph contains only the following RDF statements from the original ontology file: `rdf:type` and `rdfs:subClassOf`, which are the predicates needed for manipulating the input’s taxonomical information. The working graph is the one in which Scior is going to perform its implemented rules.

Lastly, Scior loads a reduced version of gUFO containing only Endurant Types into a new graph called **gUFO graph**. The loaded resource is named `gufoEndurantsOnly.ttl` and can be found within Scior’s [resource folder](https://github.com/unibz-core/Scior/tree/main/scior/resources). This graph is later merged with the working graph and used only for simplifying the acquisition of known gUFO information from the input ontology. If the user has set the argument for saving the gUFO ontology in the generated output file, then Scior uses the gUFO graph for this purpose.

### Working Data Structure

From the working graph, we extract all classes from the ontology and create a data structure–here called `dataclass`–for each class with the following fields:

- `uri`: the URI of the class.
- `is_type`: Known gUFO classifications that the class has. gUFO classifications that were positively asserted to the class.
- `can_type`: Unknown gUFO classifications. Classifications that may be positively or negatively asserted to the class.
- `not_type`: Known gUFO classifications that the class does not have. gUFO classifications that were negatively asserted to the class.
- `incompleteness_info`: Keeps information regarding a possible incompleteness of the class. Informs if Scior detected if the class is incomplete or not and which rules detected the incompleteness.

The `dataclass` structure has other fields, like a pointer to `gufo_dictionary`, which brings information for faster [classification manipulation](#classifications-manipulation). It also has fields related to the individuals’ hierarchy, which are currently out of scope.

During their initialization, all individual dataclasses are inserted into a list named `ontology_dataclass_list`.

### Classifications’ Manipulation

Scior has a specific operation for asserting a gUFO classification to a class. This classification happens at the moment in which one of the implemented rules identifies a new classification for one of the dataclasses in the `ontology_dataclass_list`.

Once identified of being of a certain type, Scior moves the gUFO classification from this class’s `can_type` list to its `is_type` list (in the case of a positive classification) or to its `not_type` list (in case of a negative classification). After every classification movement between lists, the inferencing method and consistency evaluation are performed.

Note that, according to the Scior’s premise II, classes cannot be reclassified. Hence, moving elements from the `is_type` list or from the `not_type` list is never an allowed operation. The absence of a necessary classification in the `can_type` list configures an inconsistency.

### Inferencing Method

The gUFO categories (i.e., its classes) are available in a hierarchical structure, having restrictions (e.g., completeness and disjointness axioms) between them.

As an example, categorizing a given class as a `gufo:Kind` also demands us to categorize it as a `gufo:Sortal`, because `gufo:Kinds` are subclasses of `gufo:Sortals` in the gUFO hierarchy of classes. In addition, the class `gufo:Sortal` is disjoint with the class `gufo:NonSortal`, meaning that the same class can also be classified as **not** a `gufo:NonSortal` and as **not** a `gufo:Role`. Each asserted knowledge can cause multiple knowledge to be inferred from it. The most common way to calculate this inferred knowledge is using reasoning engines or reasoners, for short.

[Reasoners](https://www.w3.org/2001/sw/wiki/Category:Reasoner), and in special [OWL Reasoners](https://www.w3.org/2001/sw/wiki/Category:OWL_Reasoner) usually implement various capabilities, performing multiple calculations like type inheritance, transitivity, reflexivity, inconsistency detection, etc. The more complex the ontology is, the more time the reasoner is going to need to complete all its calculations. Reasoning over a whole knowledge graph is usually a time-consuming task.

Scior has a structure that allows us to skip performing a complete reasoning task over the ontology being evaluated. First, because of its restricted scope, where only a few ontology entities are considered, just a small set of inferences is necessary. E.g., as it does not use object properties for the identification of ontological categories, it is unnecessary to perform any type of inference over them. Also, because of the restricted number of axioms that gUFO has, inferences can be manually (as we do it now) or automatically (as we intend [to do in the future](https://github.com/unibz-core/Scior/issues/5)) translated to code and then performed.

In the current version of Scior, we use [a yaml file](https://github.com/unibz-core/Scior/blob/main/scior/resources/gufo_data.yaml) (located in the `/resources/gufo_data.yaml` project’s folder) for registering all necessary inferences over gUFO entities that Scior should perform. This file contains information about each type and their specializations, and about disjointness and completeness of sets of classes. The file is loaded to a python dictionary and Scior accesses it every time it needs to perform a classification in an ontology class. I.e., it makes all necessary inferences every time a gUFO classification is moved from a class’s `can_type` list to its `is_type` or `not_type` list.

### Consistency Evaluations

Intending to ensure data consistency, Scior performs consistency evaluations multiple times during its execution. The following consistency verifications are performed for dataclasses via one of its `is_consistent` method:

- Verification of duplicates in each of its internal lists (`is_type`, `can_type`, and `not_type`), guaranteeing that the same classification is never in two lists at the same time.
- Verification of multiple final classifications, guaranteeing that two final classifications (gUFO leaf classes) cannot be in the `is_type` list together.

Scior executes the consistency evaluations for all elements of the `ontology_dataclass_list` when they are initialized, as well as every time that a gUFO classification is moved from the `can_type` to the `is_type` or `not_type` list in a dataclass.

## Rules Executions

The diagram below shows, in a very simplified manner, how Scior performs its implemented rules.

![flowchart](https://user-images.githubusercontent.com/8641647/211357509-b9bb38ec-59d8-4862-88b0-fbe7de9d1c86.png)

In this section, we are going to decompose this flowchart, explaining each step of the execution process. Regarding individual rules, we provide a complete description of each one in a [specific documentation](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-ImplementedRules.md).

### Rule Types

We separate the Scior’s rules into two categories: always automatic rules and general rules. Each of these categories has the following rules as members:

- **Always Automatic Rules:** `k_s_sup`, `s_k_sub`, `t_k_sup`, `ns_s_sup`, `s_ns_sub`, `r_ar_sup`, `ar_r_sub`, `ns_sub_r`, `ks_sf_in`, and `sub_r_r`.
- **General Rules:** `n_r_t`, `ns_s_spe`, `nk_k_sup`, `s_nsup_k`, and `nrs_ns_r`.

Clarifying this separation is important because Scior executes them in different loops. For implementing the rules’ execution logic, we created three lists of rules: two reflecting the available categories (`always_automatic_rules` and `general_rules`) and a third rule that is the concatenation of these two lists, called `list_of_rules`.

### Hashing

The hashing is an important part of the rules’ execution process, as its resulting value is used to verify if the rules performed modifications on the processed data. As presented in the image at the beginning of this section, Scior executes the rules in loops until there is no more information to be discovered–i.e., up to when the output hash is the same as the input hash.

The data structure Scior uses for creating the hash is the [`ontology_dataclass_list`](#working-data-structure). As this data structure contains all information that has been analyzed, its hash allows us to identify any modification that the rules may cause to the data.

For creating this hash value, we concatenate the values of attributes of all its composing dataclasses (i.e., the strings of their `uri`, `is_type`, `can_type`, and `not_type` lists). Finally, Scior performs the encoding through the following piece of code:

```python
enc_hash = class_hash.encode(’utf-8’)
final_hash = int(hashlib.sha256(enc_hash).hexdigest(), 16)
```

### Execution Logic

The image below details the rules’ execution process, representing the two existent loops of execution.

![rules executions small](https://user-images.githubusercontent.com/8641647/211357562-b4a5200e-50d5-4523-910d-829d082d2616.png)

The rule’s execution begins (step #1, represented in the figure by a black arrow) with the execution of only the rules classified as always automatic. Scior executes the ten rules that compose this group until they do not produce any new results when comparing the input’s hash with the output hash. Two upper rectangles in the figure above (“Execution of Always Automatic Riles” and “Evaluation Process”) represent this first loop (#2) of rules’ executions. The aim of the first loop is to reduce the necessity of human intervention, which is the most time-consuming step.

When the output hash from the ontology processing equals the input hash, the first loop is over and the second one begins (#3). This second loop is broader than the first, being composed of all four rectangles from the figure, including even the first loop (steps #3, #4, #5, and #2). This loop starts with the execution of the five general rules, which are possibly interactive rules (depending on the user’s configuration provided as an argument). Scior executes the second loop until there is no more knowledge to be discovered, accomplishing its aim, which is to guarantee that all possible knowledge discovery occurs.

### Information and Data Reporting

We can classify the data presented on screen to the user during the Scior execution in four different categories: user interaction, information, incompleteness, and inconsistencies.

#### User Interaction

User interaction is only required in for the five general rules and is only going to be required if the user runs Scior in the interactive mode (i.e., if the user does not set the software as automatic, as being interactive is the default behavior of Scior). The user is required to interact every time there is more than one option to fulfill a gUFO constraint.

The interactions required by Scior are simple, basically comprising selecting provided options. In most interactions, the user can (i) inform if a class should be classified or (ii) select a class among a list of classes to be classified into different gUFO categories, according to the rule being executed. Finally, the user can skip the selection—we provide this option for the case where the user does not know the required information. In all mentioned possibilities, Scior provides the user with basic information about the situation identified (gUFO constraint or model incompleteness) and about the involved classes.

#### Reporting Information

Besides the user interactions, other information presented on screen during the Scior’s execution are related to important execution steps (e.g., “*Starting GUFO types’ hierarchy rules ...*”), decisions took by the algorithm in certain rules (e.g., “*The class X is the unique possible identity provider for Y. Hence, it was automatically asserted as gufo:Kind*”), and confirmations. By the end of the execution, Scior presents [final statistics](#execution-statistics). In addition, the user can chose to print execution times through setting a [specific argument](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Execution-Modes.md#complementary-arguments).

#### Reporting Incompleteness

Some important pieces of information presented on screen are the incompleteness cases found during the software execution. As [incompleteness is an ontological deficiency](https://research.utwente.nl/en/publications/ontological-foundations-for-structural-conceptual-models), the automatic identification of incomplete classes is a valuable feature provided by Scior. During the execution, the software reports the incompleteness cases as warning messages and, after its end, it presents a table with incomplete classes and their respective detection rules.

Six of the Scior implemented rules can detect and report incompleteness. We present in the list below these rules and the situations that they can detect incompleteness:

- `n_r_t`: Identifies when there is no identity principle associated with a given class.
- `ns_s_spe`: Identifies when a class is associated with less than two `gufo:Kinds`.
- `nk_k_sup`: Identifies when a `gufo:Sortal` class does not have an identity provider (a direct or indirect superclass of type `gufo:Kind`).
- `s_nsup_k`: Identifies when a class does not have an identity provider.
- `nrs_ns_r` (applied only to complete models): This rule identifies when a class is `gufo:NonRigid` and `gufo:Sortal` without siblings, stating that the class must be set as a `gufo:Role`. It also informs that if the class is a `gufo:Phase`, at least another `gufo:Phase` sibling class is missing, representing an incompleteness.
- `ks_sf_in`: As phases always occur in phase partitions, this rule identifies when a class is the only `gufo:Phase` subclass of another given class.

Note that the ontology modeler must not always solve all cases of incompleteness, as some models may present incompleteness because of the level of abstraction adopted by their modelers. Also, incompleteness only occurs in models that are set as incomplete by the user. If the user states that the model is complete using the [specific argument](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Execution-Modes.md#models-completeness-modes) for that, then the mentioned problems are not incompleteness, but **inconsistencies**.

#### Reporting Inconsistencies

Differently from incompleteness, inconsistencies are not a type of ontological deficiency, but an invalid state that invalidates the execution of the software. In simple terms, it is an error that the ontology has and, hence, Scior reports these cases with error messages and aborts its execution so the ontology modeler can solve the problem.

In Scior, an inconsistency is detected whenever a type has to be set and the software does not find it as a valid option. I.e., Scior tries to move the type from the `can_type` to the `is_type` or to the `not_type` list, but the type is not available in the `can_type` list. Unfortunately, the current version of the software does not clearly specify the problem that caused the inconsistency in most cases—however, this is [a known issue](https://github.com/unibz-core/Scior/issues/7) that is going to be addressed soon.

The first example of inconsistencies that we can mention are the ones we presented in the past section, the ones that happen when a user sets an incomplete model as complete. The other cases are mainly related to incorrect information inputted to the software (e.g., the input ontology has a class of type `gufo:Kind` with a subclass of the same type). Finally, note that the information provided by the user during the interaction rules can also lead to invalid states, generating inconsistencies. We tried to avoid this last situation as much as possible with the creation of restriction rules. However, because of the iterative coding, it may happen.

## Output Files

This section presents information about the output files generated by Scior, which are the ontology added with the discovered ontological classifications, and the execution report file. Scior also creates a log file in a folder called `logs` inside the project’s folder, but the description of this file is out of this document’s scope.

### Output Ontology

After the Scior execution, all knowledge discovered through the execution of gUFO rules are added to the working graph (i.e., to the input ontology graph) and this complete graph is saved as a *ttl* file. The file is saved into the same folder as the input file using the following file nomenclature: `example-{YYYY.MM.DD-hh.mm.ss}.out.ttl`, where “example” is the name of the ontology and the curly brackets are substituted by year (Y), month (M), day (D), hour (h), minutes (m), and seconds (s) of the end of the execution.

By default, Scior registers only the new statements that make the ontology classes instances of gUFO types (in the format `ontology_class rdf:type gufo_class`) in the output file. It is also possible to import gUFO or even save all its statements in the output file [by using specific arguments](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Execution-Modes.md#complementary-arguments).

### Report File

Scior generates a complete report file after concluding an execution. The report contains information about the execution itself and about the situation before and after its conclusion. The information presented in the report is:

- **Execution Information:** displays general and specific (per rule) execution times, together with computer and software specifications, used configurations, generated files and solution’s hashes.
  - The software creates solutions’ hashes so the user can quickly verify if the results have changed from one execution to another.
- **Lists of Classes Before Scior:** displays the classes grouped according to the amount of gUFO knowledge known **before** the Scior execution. I.e., it presents the **initial** state of the ontology that is going to be evaluated.
  - The categories used for grouping the classes are: Totally Unknown Classes, Partially Known Classes, and Totally Known Classes.
- **Lists of Classes After Scior:** displays the classes grouped according to the amount of gUFO knowledge known **after** the Scior execution. I.e., it presents the **final** state of the ontology that was evaluated.
  - The categories used for grouping the classes are: Totally Unknown Classes, Partially Known Classes, and Totally Known Classes.
- **Results` Statistics:** presents tables with total numbers and percentages of classes and classifications before the execution, after the execution, and the difference between these two situations.
  - The [next subsection](#execution-statistics) details the information about the presented statistics.
- **Incomplete Classes Identified:** presents a table containing all classes identified as incomplete together with the implemented rules that were responsible for that identification.
- **Knowledge Matrix:** As there are 14 gUFO Endurant Types, the knowledge matrix is a 15x15 matrix. Each matrix element indicates a QUANTITY of classes: the rows`index (from 0 to 14) indicates how many known types **before** the execution, and the columns` index (from 0 to 14) Shows how many known types **after** the execution. The position (ROW, COL) indicates how many classes began with ROW known types and ended with COL known types.
  - As instance, if matrix position (0,5) stores the value 17, it means that 17 classes started the evaluation (i.e., the user provided them as input) without known classifications and these classes finished (i.e., Scior provided them as output) with 5 known gUFO types.
- **Final Classes’ Classifications:** presents the complete internal gUFO classifications’ lists (`is_type`, `can_type`, and `not_type`) for each class, sorted by their URI. With this information, the user can know the final classification of each one of the ontology classes.

The user can access the generated report, saved in [Markdown](https://www.markdownguide.org/basic-syntax/) format, at the `reports` folder inside Scior’s project folder.

## Execution Statistics

Scior presents to the user statistics about its current execution in two different forms: on screen and in the report file. The statistics are about data measured **before** and **after** the software’s execution and about the **difference** between these values. Their presentation contains the value of the item being measured and this value’s percentage with relation to its total amount.

You can find below an example of the statistics that are presented after the Scior’s execution:

```markdown
Results of Scior execution when evaluating 34 CLASSES considering only TYPES:
|              Evaluation |         Before |          After |     Difference |
|------------------------:|---------------:|---------------:|---------------:|
| Totally unknown classes |    30 (88.24%) |     9 (26.47%) |  -21 (-61.76%) |
| Partially known classes |       0 (0.0%) |    10 (29.41%) |    10 (29.41%) |
|   Totally known classes |     4 (11.76%) |    15 (44.12%) |    11 (32.35%) |

Results of Scior execution when evaluating 476 CLASSIFICATIONS considering only TYPES:
|              Evaluation |         Before |          After |     Difference |
|------------------------:|---------------:|---------------:|---------------:|
| Unknown classifications |   420 (88.24%) |   196 (41.18%) | -224 (-47.06%) |
|   Known classifications |    56 (11.76%) |   280 (58.82%) |   224 (47.06%) |
```

As you can see above, the presentation displays data about two items: the number of **classes** and **classifications**.

The first item presented is the number of classes that were evaluated. Scior presents it according to three classifications, which are the number of:

- Totally Unknown Classes: classes that do not have relations to any gUFO concept.
- Partially Known Classes: classes that have relation to higher-level gUFO concepts, but that are not yet fully classified.
- Totally Known Classes: classes that have relation to higher-level gUFO classifications. I.e., classes that have their classifications totally known.

Regarding classifications, these are the gUFO classes (e.g., `gufo:Kind`, `gufo:Sortal`, `gufo:RigidType`) to which an OWL ontology concept can be mapped (for endurant types, this is done via an `rdf:type` predicate). Knowledge about classifications: the number of known and of unknown classifications, as well as the total number, which is the sum of the first two ones.
