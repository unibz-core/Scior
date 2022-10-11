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