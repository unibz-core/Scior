# OntCatOWL

Identification of Ontological Categories for OWL Ontologies.

## Table of Contents

<!-- TOC -->

* [Software requirements](#software-requirements)
* [Code Execution](#code-execution)
* [Usage](#usage)
* [Software Functioning](#software-functioning)
    * [Rules Premises](#rules-premises)
* [Software Limitations](#software-limitations)
    * [Version X (to be completed)](#version-x--to-be-completed-)
* [Release Notes](#release-notes)
    * [Release 1](#release-1)

<!-- TOC -->

## Software Requirements

You need to [download and install Python](https://www.python.org/downloads/) for executing **OntCatOWL**. The code was
developed and tested using [Python](https://www.python.org/) v3.11.0

The following external libraries are necessary:

- [RDFLib](https://pypi.org/project/rdflib/) - version ~= 6.2.0
- [OWL-RL](https://pypi.org/project/owlrl/) - version ~= 6.0.2
- [PyYAML](https://pypi.org/project/PyYAML/) - version ~= 6.0
- [PrettyTable](https://pypi.org/project/prettytable/) - version ~= 3.4.1

For installing them, run the following command on the terminal:

```shell
pip install -r requirements.txt
```

## Code Execution

After the external libraries are installed, run the following command on the terminal for executing **OntCatOWL**:

```shell
python ontcatowl.py <input file OR URL>
```

## Usage

```
usage: OntCatOWL [-h] [-i | -a] [-n | -c] [-r] [-t] [-g] [-v] ontology_file

positional arguments:
  ontology_file      The path of the ontology file to be loaded.

options:
  -h, --help         show this help message and exit
  -i, --interactive  Executes automatic rules whenever possible. Executes interactive rules only if necessary.
  -a, --automatic    Executes only automatic rules. Interactive rules are not performed.
  -n, --incomplete   The loaded ontology is an incomplete model.
  -c, --complete     The loaded ontology is a complete model.
  -r, --reasoning    Enable RDF reasoning for graph expansion.
  -t, --times        Prints the execution times of all functions.
  -g, --gufo         Imports GUFO ontology in the output ontology file.
  -v, --version      Prints the software version and exit.
```

The input file syntax is automatically detected by the **OntCatOWL**.

## Software Functioning

### Rules Premises

- new classes cannot be created during the execution of OntCatOWL.
- all stereotypes already set as is or not are immutable. i e., there can be no movement from lists is or not.
- When interactivity is enabled, interactions are only available when there are more than one option.

## Software Limitations

### Version X (to be completed)

- Disjoint and Complete are not supported.

## Release Notes

### Release 1

## Contributors

- PhD. Pedro Paulo Favato
  Barcelos [[GitHub]](https://github.com/pedropaulofb) [[LinkedIn]](https://www.linkedin.com/in/pedro-paulo-favato-barcelos/)
- PhD. Tiago Prince
  Sales [[GitHub]](https://github.com/tgoprince) [[LinkedIn]](https://www.linkedin.com/in/tiago-sales/)
- MSc. Elena Romanenko [[GitHub]](https://github.com/mozzherina) [[LinkedIn]]()
- Prof. PhD. Giancarlo Guizzardi [[LinkedIn]](https://www.linkedin.com/in/giancarlo-guizzardi-bb51aa75/)
- MSc. Gal Engelberg [[GitHub]]() [[LinkedIn]](https://www.linkedin.com/in/gal-engelberg/)
- Prof. PhD. Dan Klein [[LinkedIn]](https://www.linkedin.com/in/~danklein/)

## Acknowledgements

This work is a collaboration with Accenture Israel Cybersecurity Labs.