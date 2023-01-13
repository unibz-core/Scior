# OntCatOWL: Identification of Ontological Categories for OWL Ontologies

**[OntCatOWL](https://github.com/unibz-core/OntCatOWL)** is the abbreviated name for Identification of Ontological Categories for OWL Ontologies, a Python command-line software that aims to support the semi-automatic semantic improvement of lightweight web ontologies. We aim to reach the referred semantic improvement via the association of [gUFO](https://nemo-ufes.github.io/gufo/)—a lightweight implementation of the [Unified Foundational Ontology (UFO)](https://nemo.inf.ufes.br/wp-content/uploads/ufo_unified_foundational_ontology_2021.pdf)—concepts to the OWL entities. The aim of gUFO is “*to provide a lightweight implementation of the Unified Foundational Ontology (UFO) suitable for Semantic Web OWL 2 DL applications*”.

## Contents

- [Functioning and Features](#functioning-and-features)
- [Installation Requirements](#installation-requirements)
- [Execution Options](#execution-options)
- [Related Repositories](#related-repositories)
- [Contributors](#contributors)
- [Acknowledgements](#acknowledgements)

## Functioning and Features

We provide specific documentation for better explaining the OntCatOWL scope, objectives, functioning logics, and features. Please access the following links for more information.

- [Functioning Overview](https://github.com/unibz-core/OntCatOWL/blob/main/documentation/OntCatOWL-Functioning.md)
- [Execution Modes](https://github.com/unibz-core/OntCatOWL/blob/main/documentation/OntCatOWL-Execution-Modes.md)
- [Implemented Rules](https://github.com/unibz-core/OntCatOWL/blob/main/documentation/OntCatOWL-ImplementedRules.md)

## Installation Requirements

You need to [download and install Python](https://www.python.org/downloads/) for executing **OntCatOWL**. The code was developed and tested using [Python](https://www.python.org/) v3.11.0. For installing the required libraries, run the following command on the terminal:

```txt
pip install -r requirements.txt
```

If you would like to use the project as a package, run the following command on the terminal:

```txt
pip install git+https://github.com/unibz-core/OntCatOWL.git
```

## Execution Options

With all the requirements installed, you can run OntCatOWL in diverse modes. For accessing this information, please execute the following command inside the project’s folder:

```txt
python ontcatowl -h
```

After executing the command above, OntCatOWL will provide all its usages and valid arguments, which are:

```txt
usage: ontcatowl [-h] [-i | -a] [-n | -c] [-r] [-t] [-g1] [-g2] [-v] ontology_file

OntCatOWL - Identification of Ontological Categories for OWL Ontologies

positional arguments:
ontology_file The path of the ontology file to be loaded.

options:
-h, --help          Show this help message and exit.
-i, --interactive   Executes automatic rules whenever possible. Executes interactive rules only if necessary.
-a, --automatic     Executes only automatic rules. Interactive rules are not performed.
-n, --incomplete    The loaded ontology is an incomplete model.
-c, --complete      The loaded ontology is a complete model.
-r, --reasoning     Enable RDF reasoning for graph expansion.
-t, --times         Prints the execution times of all functions.
-g1, --gufo1        Imports gUFO ontology in the output ontology file.
-g2, --gufo2        Saves all gUFO statements in the output ontology file.
-v, --version       Prints the software version and exit.
```

You can find more information about the execution options in the [related documentation file](https://github.com/unibz-core/OntCatOWL/blob/main/documentation/OntCatOWL-Execution-Modes.md).

**IMPORTANT:** Please note that because of a problem [registered in this open issue](https://github.com/unibz-core/OntCatOWL/issues/11), the software may not be executed as we here present it.

## Related Repositories

The [OntCatOWL-Tester](https://github.com/unibz-core/OntCatOWL-Tester) is a software developed with two main purposes: (i) to build the infrastructure for running multiple OntCatOWL tests on the OntoUML/UFO Catalog datasets; and (ii) to be the place where these tests are implemented and executed from.

The FAIR Model Catalog for Ontology-Driven Conceptual Modeling Research, short-named [OntoUML/UFO Catalog](https://github.com/unibz-core/ontouml-models), is a structured and open-source catalog that contains OntoUML and UFO ontology models. The catalog was conceived to allow collaborative work and to be easily accessible to all its users. Its goal is to support empirical research in OntoUML and UFO, as well as for the general conceptual modeling area, by providing high-quality curated, structured, and machine-processable data on why, where, and how different modeling approaches are used. The catalog offers a diverse collection of conceptual models, created by modelers with varying modeling skills, for a range of domains, and for different purposes.

Results of the tests performed using the OntCatOWL-Tester are available at the [OntCatOWL-Dataset](https://github.com/unibz-core/OntCatOWL-Dataset). The aim of the publication of the resulting datasets is to share with the community data that can be analyzed in different ways, even though all executed tests are totally reproducible.

In short:

- [OntCatOWL](https://github.com/unibz-core/OntCatOWL): software for identification of ontological categories for OWL ontologies.
- [OntCatOWL-Tester](https://github.com/unibz-core/OntCatOWL-Tester): used for automating tests on OntCatOWL.
- [OntCatOWL-Dataset](https://github.com/unibz-core/OntCatOWL-Dataset): contains data resulting from the OntCatOWL-Tester.
- [OntoUML/UFO Catalog](https://github.com/unibz-core/ontouml-models): source of models used for the performed tests.

## Contributors

- PhD. Pedro Paulo Favato Barcelos [[GitHub]](https://github.com/pedropaulofb) [[LinkedIn]](https://www.linkedin.com/in/pedro-paulo-favato-barcelos/)
- PhD. Tiago Prince Sales [[GitHub]](https://github.com/tgoprince) [[LinkedIn]](https://www.linkedin.com/in/tiago-sales/)
- MSc. Elena Romanenko [[GitHub]](https://github.com/mozzherina)
- Prof. PhD. Giancarlo Guizzardi [[LinkedIn]](https://www.linkedin.com/in/giancarlo-guizzardi-bb51aa75/)
- Eng. MSc. Gal Engelberg [[GitHub]](https://github.com/GalEngelberg) [[LinkedIn]](https://www.linkedin.com/in/gal-engelberg/)
- MBA Dan Klein [[GitHub](https://github.com/danklein10)] [[LinkedIn](https://www.linkedin.com/in/~danklein/)]

Please get in touch with this software’s contributors using the provided links or **preferably** [open an issue](https://github.com/unibz-core/ontouml-models-tools/issues/) in case of doubts or problems found.

## Acknowledgements

This work is a collaboration with Accenture Israel Cybersecurity Labs.
