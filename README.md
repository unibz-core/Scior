# Scior: Enhancing the Semantics of OWL Ontologies Using Rule-based Alignment with Foundational Ontologies

<p align="center"><img src="https://user-images.githubusercontent.com/8641647/223773249-9a5b4f97-caf2-42ea-ac36-a7b7290be58e.png" width="500">

**[Scior](https://github.com/unibz-core/Scior)** is a Latin word meaning "_I am known_". This software implements Identification of Ontological Categories for OWL Ontologies, a Python command-line software that aims to support the semi-automatic semantic improvement of lightweight web ontologies. We aim to reach the referred semantic improvement via the association of [gUFO](https://nemo-ufes.github.io/gufo/)—a lightweight implementation of the [Unified Foundational Ontology (UFO)](https://nemo.inf.ufes.br/wp-content/uploads/ufo_unified_foundational_ontology_2021.pdf)—concepts to the OWL entities. The aim of gUFO is “_to provide a lightweight implementation of the Unified Foundational Ontology (UFO) suitable for Semantic Web OWL 2 DL applications_”.

## Contents

  - [Functioning and Features](#functioning-and-features)
  - [Installation Requirements](#installation-requirements)
  - [Execution Options](#execution-options)
  - [Related Repositories](#related-repositories)
  - [Publications and 'How to Cite'](#publications-and-how-to-cite)
  - [Contributors](#contributors)
  - [Acknowledgments](#acknowledgments)

## Functioning and Features

We provide specific documentation for better explaining the Scior scope, objectives, functioning logics, and features. Please access the following links for more information.

<!-- - [Functioning Overview](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Functioning.md) -->
<!-- - [Execution Modes](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Execution-Modes.md) -->
- [Theoretical Rules](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Theoretical-Rules.md)
- [Implemented Rules Definitions](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Implemented-Rules-Definitions.md)
<!-- - [Implemented Rules Actions](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Implemented-Rules-Actions.md) -->
- [Tests](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Tests.md)

## Installation Requirements

You need to [download and install Python](https://www.python.org/downloads/) for executing **Scior**. The code was developed and tested using [Python](https://www.python.org/) v3.11.0. For installing the required libraries, run the following command on the terminal:

```txt
pip install -r requirements.txt
```

If you would like to use the project as a package, run the following command on the terminal:

```txt
pip install git+https://github.com/unibz-core/Scior.git
```

## Execution Options

With all the requirements installed, you can run Scior in diverse modes. For accessing this information, please execute
the following command inside the project’s folder:

```txt
python scior -h
```

After executing the command above, Scior will provide all its usages and valid arguments, which are:

```txt
usage: scior [-h] [-i | -a] [-cwa | -owa | -owal] [-s | -r | -d]
             [-gr | -gi | -gw] [-v]ontology_file

Scior - Identification of Ontological Categories for OWL Ontologies

positional arguments:
  ontology_file         The path of the ontology file to be loaded.

options:
  -h, --help            show this help message and exit
  -i, --interactive     Execute automatic rules whenever possible, interactive
                        rules when necessary.
  -a, --automatic       * Execute only automatic rules. Interactive rules are
                        not performed.
  -cwa, --is_cwa        Operate in Closed-World Assumption (CWA).
  -owa, --is_owa        * Operate in Open-World Assumption (OWA) - Regular
                        Mode.
  -owal, --is_owa_light
                        Operate in Open-World Assumption (OWA) - Light Mode.
  -s, --silent          Silent mode. Print only basic execution status
                        information.
  -r, --verbose         * Print basic execution information and results.
  -d, --debug           Generates tons of log for debugging.
  -gr, --gufo_results   * Write in the output ontology file only the gUFO
                        classifications found.
  -gi, --gufo_import    Import gUFO ontology in the output ontology file.
  -gw, --gufo_write     Write all gUFO statements in the output ontology file.
  -v, --version         Print the software version and exit.

Asterisks represent default values.
```

You can find more information about the execution options in the [related documentation file](https://github.com/unibz-core/Scior/blob/main/documentation/Scior-Execution-Modes.md).

## Related Repositories

The [Scior-Tester](https://github.com/unibz-core/Scior-Tester) is a software developed with two main purposes: (i) to build the infrastructure for running multiple Scior tests on the OntoUML/UFO Catalog datasets; and (ii) to be the place where these tests are implemented and executed from.

The FAIR Model Catalog for Ontology-Driven Conceptual Modeling Research, short-named [OntoUML/UFO Catalog](https://github.com/unibz-core/ontouml-models), is a structured and open-source catalog that contains OntoUML and UFO ontology models. The catalog was conceived to allow collaborative work and to be easily accessible to all its users. Its goal is to support empirical research in OntoUML and UFO, as well as for the general conceptual modeling area, by providing high-quality curated, structured, and machine-processable data on why, where, and how different modeling approaches are used. The catalog offers a diverse collection of conceptual models, created by modelers with varying modeling skills, for a range of domains, and for different purposes.

Results of the tests performed using the Scior-Tester are available at the [Scior-Dataset](https://github.com/unibz-core/Scior-Dataset). The aim of the publication of the resulting datasets is to share with the community data that can be analyzed in different ways, even though all executed tests are totally reproducible.

In short:

- [Scior](https://github.com/unibz-core/Scior): software for identification of ontological categories for OWL
  ontologies.
- [Scior-Tester](https://github.com/unibz-core/Scior-Tester): used for automating tests on Scior.
- [Scior-Dataset](https://github.com/unibz-core/Scior-Dataset): contains data resulting from the Scior-Tester.
- [OntoUML/UFO Catalog](https://github.com/unibz-core/ontouml-models): source of models used for the performed tests.

## Publications and 'How to Cite'

Please use the following reference to cite this work:

- *Barcelos, P. P. F., Sales, T. P., Romanenko, E., Almeida, J. P. A., Engelberg, G., & Klein, D. (2023). Inferring Ontological Categories of OWL Classes Using Foundational Rules. 13th International Conference on Formal Ontology in Information Systems (FOIS 2023). <https://purl.org/scior>*

**Abstract:** Several efforts that leverage the tools of formal ontology (such as OntoClean, OntoUML, and UFO) have demonstrated the fruitfulness of considering key metaproperties of classes in ontology engineering. These metaproperties include sortality, rigidity, and external dependence, and give rise to many fine-grained ontological categories for classes, including, among others, kinds, phases, roles, mixins, etc. Despite that, it is still common practice to apply representation schemes and approaches---such as OWL---that do not benefit from identifying these ontological categories, and simplistically treat all classes in the same manner. In this paper, we propose an approach to support the automated classification of classes into the ontological categories underlying the (g)UFO foundational ontology. We propose a set of inference rules derived from (g)UFO's axiomatization that, given an initial classification of the classes in an OWL ontology, can support the inference of the classification for the remaining classes in the ontology. We formalize these rules, implement them in a computational tool and assess them against a catalog of ontologies designed by a variety of users for a number of domains.

The full paper can be [downloaded here](https://www.researchgate.net/publication/370527243_Inferring_Ontological_Categories_of_OWL_Classes_Using_Foundational_Rules).

## Contributors

- [Pedro Paulo F. Barcelos](https://orcid.org/0000-0003-2736-7817) [[GitHub]](https://github.com/pedropaulofb) [[LinkedIn]](https://www.linkedin.com/in/pedro-paulo-favato-barcelos/)
- [Tiago Prince Sales](https://orcid.org/0000-0002-5385-5761) [[GitHub]](https://github.com/tgoprince) [[LinkedIn]](https://www.linkedin.com/in/tiago-sales/)
- [Elena Romanenko](https://orcid.org/0000-0002-8139-5977) [[GitHub]](https://github.com/mozzherina)
- [Giancarlo Guizzardi](https://orcid.org/0000-0002-3452-553X) [[LinkedIn]](https://www.linkedin.com/in/giancarlo-guizzardi-bb51aa75/)
- [João Paulo A. Almeida](https://orcid.org/0000-0002-9819-3781) [[GitHub]](https://github.com/jpalmeida)
- Gal Engelberg [[GitHub]](https://github.com/GalEngelberg) [[LinkedIn]](https://www.linkedin.com/in/gal-engelberg/)
- Dan Klein [[GitHub]](https://github.com/danklein10) [[LinkedIn]](https://www.linkedin.com/in/~danklein/)

Please get in touch with this software’s contributors using the provided links or **preferably [open an issue](https://github.com/unibz-core/ontouml-models-tools/issues/)** in case of doubts or problems found.

## Acknowledgments

This work is a collaboration with Accenture Israel Cybersecurity Labs.
