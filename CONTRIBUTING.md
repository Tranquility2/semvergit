  ### Code Style and Linting
  Please use The following tools  for code style and linting:
  - Black
  - Isort
  - Pylint
  - Mypy

  All are configured in the  Pyproject.toml file
  Pre-commit hooks are configured  to run these tools  automatically on commit.
  Please install them by running:  ``pre-commit install``

  ### Testing
  Please use pytest for testing.  Run tests with ``make tests``.

  ### Workflow
  This repo uses the [Trunk Based Development](https:/trunkbaseddevelopment.com)  workflow.

  ### Branching
  The main branch is `main`.
  All development should be done  in feature branches and merged  into `main` via pull requests.

  ### Versioning
  This repo uses [Semantic Versioning](https://semver.org/).
