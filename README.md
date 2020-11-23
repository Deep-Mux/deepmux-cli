# Command-line tool: installation

## Pre-requisites

### Python

Install Python 3.6 or older. Follow the  [instruction here](https://wiki.python.org/moin/BeginnersGuide/Download).
Skip this step if you already have proper version of python installed.

### Pip

We are going to use `pip` to install deepmux command line interface below. If you don't have `pip` available from the command line, follow [this guide](https://pip.pypa.io/en/stable/installing/).

### Optional: virtualenv

Install `virtualenv` module if you don't have it already:

```
pip3 install virtualenv
```

Then create one:
```
virtualenv venv
```

And activate:
```
source venv/bin/activate
```

## Installing and configure the package

### Install

Use `pip` to install `deepmux-cli`:
```
pip3 install deepmux-cli
```

### Login

Go to the [https://app.deepmux.com/api_key](https://app.deepmux.com/api_key) and copy your token.

Than run:
```
deepmux login
```
And paste your token below.

Run `--help` to see the full list of options:
```
deepmux --help
``` 

## That's it!

If you have any questions feedback please send it at [dev@deepmux.com](mailto:dev@deepmux.com)

Thank you!

![](https://i.imgur.com/UMMcZNg.jpg)
