|||
|-|-|
| CI/CD   | [![Pytest](https://github.com/Tranquility2/semvergit/actions/workflows/pytest.yml/badge.svg)](https://github.com/Tranquility2/semvergit/actions/workflows/pytest.yml) [![Publish](https://github.com/Tranquility2/semvergit/actions/workflows/publish.yml/badge.svg)](https://github.com/Tranquility2/semvergit/actions/workflows/publish.yml) ![GitHub Latest Release)](https://img.shields.io/github/v/release/Tranquility2/semvergit?logo=github) [![Coverage Status](https://coveralls.io/repos/github/Tranquility2/semvergit/badge.svg)](https://coveralls.io/github/Tranquility2/semvergit) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)| 
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/semvergit.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/semvergit/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/semvergit.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/semvergit/) [![Downloads](https://img.shields.io/pypi/dm/semvergit.svg?logo=python&label=PyPI&logoColor=gold)](https://pepy.tech/project/semvergit) |
| Meta    | [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) [![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint) [![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/) |

# semvergit
![semvergit](https://raw.githubusercontent.com/Tranquility2/semvergit/master/assets/semvergit-255.png)

semvergit is a CLI tool to manage your project's version numbers.
It uses [Semantic Versioning](https://semver.org/) to bump the version number.
The supported bump types are:

- `major`
- `minor`
- `patch`
- `prerelease`

## Internal Workflow
___What's actully happening when you run this tool___
1. Use the latest git tag to determine the current version number.
2. Bump the version number
3. Create a new git tag
4. Push the tag to the remote

## Why?
I created this tool to help me manage my project's version numbers.
I wanted a simple tool that I could use in my CI/CD pipeline to bump the version number and tag the commit.

## Features
❇️ Bump the version number and update the git tag in one command  
❇️ Dry run mode  
❇️ Verbose mode  
❇️ Custom commit message*  
❇️ Auto commit message*  
🆕 Version 0.4+ introduces the ability to automatically update the version number in a file*

<sup>*Please see the [limitations](#Limitations) section below</sup>

## How to use

Simple install using
``pip install semvergit``

Then you can use it in your project as simply as:
``semvergit -t patch -v``
(to bump the patch version)
This will:

1. create the relvant tag (in this case a patch bump 0.0.x -> 0.0.x+1)
2. push it to the remote

Please checkout ``semvergit --help`` for more info.

```shell
Usage: semvergit [OPTIONS] COMMAND [ARGS]...

  CLI for semvergit.

Options:
  --version                Show the version and exit.
  -d, --dry_run            Dry run
  -v, --verbose            Verbose level  [0<=x<=2]
  -t, --bump_type TEXT     Bump Type ['major', 'minor', 'patch', 'prerelease']
  -m, --message TEXT       Commit message
  -am, --auto_message      Auto commit message
  -f, --version_file FILE  Version file
  --help                   Show this message and exit.
```

## Limitations
Please keep in mind that when using features like `commit message` / `auto commit message` and `version file` the tool will try and commit the changes to the git repo.

Even though this is quite handy, it should be used mannually as it **cannot be used directly in a CI/CD pipeline directed at `master` or `main` branches** as it will likly fail due to the commit not being allowed without a PR.

💡 Only git tags can be pushed to the remote without a PR *(and this is the main use case for this tool)*.

## Development

Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## License

This project is published under the MIT license.

If you do find it useful, please consider contributing your changes back upstream.
