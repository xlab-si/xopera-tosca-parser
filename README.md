# xOpera TOSCA parser
TOSCA YAML parser for xOpera orchestrator.

[![cicd](https://github.com/xlab-si/xopera-tosca-parser/actions/workflows/ci_cd.yaml/badge.svg)](https://github.com/xlab-si/xopera-tosca-parser/actions/workflows/ci_cd.yaml)
[![PyPI](https://img.shields.io/pypi/v/opera-tosca-parser)](https://pypi.org/project/opera-tosca-parser/)
[![Test PyPI](https://img.shields.io/badge/test%20pypi-dev%20version-blueviolet)](https://test.pypi.org/project/opera-tosca-parser/)

## Table of Contents
  - [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
  - [Installation and Quickstart](#installation-and-quickstart)
  - [License](#license)
  - [Contact](#contact)
  - [Acknowledgement](#acknowledgement)

## Introduction
xOpera TOSCA parser aims to be a lightweight parser component compliant with [OASIS TOSCA]. 
The current compliance is with the [OASIS TOSCA Simple Profile in YAML v1.3].

## Prerequisites
`opera-tosca-parser` requires Python 3 and a virtual environment. 
In a typical modern Linux environment, we should already be set. 
In Ubuntu, however, we might need to run the following commands:

```console
$ sudo apt update
$ sudo apt install -y python3-venv python3-wheel python-wheel-common
```

## Installation and Quickstart
The orchestration tool is available on PyPI as a package named [opera-tosca-parser]. 
Apart from the latest [PyPI production] version, you can also find the latest [PyPI development] version, which 
includes pre-releases so that you will be able to test the latest features before they are officially released.

The simplest way to test `opera-tosca-parser` is to install it into Python virtual environment:

```console
$ python3 -m venv .venv && . .venv/bin/activate
(.venv) $ pip install opera-tosca-parser
```

To test if everything is working as expected, you can clone [xopera-examples] GitHub repository and try to parse a 
simple [hello-world] example with the `opera-tosca-parser` CLI tool that comes along with the TOSCA parser:

```console
(.venv) $ git clone git@github.com:xlab-si/xopera-examples.git
(.venv) $ cd xopera-examples/misc/hello-world
(.venv) $ opera-tosca-parser parse service.yaml
Parsing service template...
Done.
```

And that is it. 
The `opera` orchestrator is available in [xopera-opera] repository.
For more startup examples please visit [xopera-examples] repository.
If you want to use opera commands from an API take a look at [xopera-api] repository. 
You can also take a look at the [xOpera SaaS] component, which is designed for business partners and enterprise users.
To find more about xOpera project visit our [xOpera documentation].

## License
This work is licensed under the [Apache License 2.0].

## Contact
You can contact the xOpera team by sending an email to [xopera@xlab.si].

## Acknowledgement
Some work from this project has received funding from the European Union’s Horizon 2020 research and innovation 
programme under Grant Agreements No. 825040 ([RADON]), No. 825480 ([SODALITE]) and No. 101000162 ([PIACERE]).

[opera-tosca-parser]: https://pypi.org/project/opera-tosca-parser/
[OASIS TOSCA Simple Profile in YAML v1.3]: https://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.3/TOSCA-Simple-Profile-YAML-v1.3.html
[xOpera documentation]: https://xlab-si.github.io/xopera-docs/
[xopera@xlab.si]: mailto:xopera@xlab.si
[OASIS TOSCA]: https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=tosca
[PyPI production]: https://pypi.org/project/opera-tosca-parser/#history
[PyPI development]: https://test.pypi.org/project/opera-tosca-parser/#history
[hello-world]: https://github.com/xlab-si/xopera-examples/tree/master/misc/hello-world
[xopera-opera]: https://github.com/xlab-si/xopera-opera
[xopera-examples]: https://github.com/xlab-si/xopera-examples
[xopera-api]: https://github.com/xlab-si/xopera-api
[xOpera SaaS]: https://xlab-si.github.io/xopera-docs/saas.html
[Apache License 2.0]: https://www.apache.org/licenses/LICENSE-2.0
[RADON]: http://radon-h2020.eu
[SODALITE]: http://www.sodalite.eu/
[PIACERE]: https://www.piacere-project.eu/
