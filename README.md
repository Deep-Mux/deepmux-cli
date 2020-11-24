# deepmux-cli

![](https://img.shields.io/pypi/pyversions/deepmux-cli)

DeepMux CLI allows to manage functions on DeepMux cloud platform.

## Pre-requisites

### Python

Install Python 3.6 or newer. Follow the  [instruction here](https://wiki.python.org/moin/BeginnersGuide/Download).

Skip this step if you already have proper version of python installed.

### Pip

We are going to use `pip` to install deepmux command line interface below. If you don't have `pip` available from the command line, follow [this guide](https://pip.pypa.io/en/stable/installing/).

## Installing and configuring the package

### Install

Use `pip` to install `deepmux-cli`:
```bash
pip install deepmux-cli
```

### Login

Go to the [https://app.deepmux.com/api_key](https://app.deepmux.com/api_key) and copy your token.

Then run:
```bash
deepmux login
```
And paste your token when prompted.

Run `--help` to see the full list of options:
```bash
deepmux --help
``` 

## Documentation

Complete documentation for deepmux-cli is availible at [deep-mux.github.io](https://deep-mux.github.io)