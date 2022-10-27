# OntCatOWL

Identification of ontological categories for OWL ontologies.

## Software requirements

You need to [download and install Python](https://www.python.org/downloads/) for executing **OntCatOWL**. The code was
developed and tested using [Python](https://www.python.org/) v3.10.5.

The following external libraries are necessary:

- [RDFLib](https://pypi.org/project/rdflib/) (version ~= 6.2.0).
- [PyYAML](https://pypi.org/project/PyYAML/) (version ~= 6.0).

For installing them, run the following command on the terminal:

```shell
pip install -r requirements.txt
```

## Code execution

After the external libraries are installed, run the following command on the terminal for executing **OntCatOWL**:

```
python ontcatowl.py <input file OR URL>
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