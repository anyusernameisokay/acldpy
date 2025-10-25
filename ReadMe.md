# acld

[![PyPI](https://img.shields.io/pypi/v/project-name.svg)](https://pypi.org/project/project-name)
[![Python](https://img.shields.io/pypi/pyversions/project-name.svg)]()
[![License](https://img.shields.io/pypi/l/project-name.svg)]()

## Summary

This Python 3 package assigns letters to indicate statistically significant
differences between groups following pairwise comparisons. It strives to be
compatiple with all major Python statistics librairies.
<br><br>
<strong> acld = agnostic compact letter display </strong>
<br><br>
Users conduct their statistical test with the library of their choice. Then,
they pass their result to run_cld. <br>
The package implements algorithms that were described by Hans-Peter Piepho
and coworkers [1,2].

## Development & Planned Features

The project is in its early development. Currently, it relies on the users
to specify which groups should should be compared against each other. In
the future, acld should detect these details automatically.
<br><br>
Furthermore, the improvements are planned:

- Different and custom alternatives to the classical small letters.
- Assigning the letters according to the numerical values of the groups.
- Optimal utilization of numpy under the hood.

## References

[1]
J. Gramm, J. Guo, F. Hüffner, R. Niedermeier, H.-P. Piepho, and R. Schmid,
“Algorithms for compact letter displays: Comparison and evaluation,”
Computational Statistics & Data Analysis, vol. 52, no. 2, pp. 725–736,
Oct. 2006,
<a href="https://doi.org/10.1016/j.csda.2006.09.035">doi: 10.1016/j.csda.2006.09.035.</a>

[2]
H.-P. Piepho, “An algorithm for a Letter-Based representation of
All-Pairwise comparisons,” Journal of Computational and Graphical Statistics,
vol. 13, no. 2, pp. 456–466, Jun. 2004,
<a href= "https://doi.org/10.1198/1061860043515">doi: 10.1198/1061860043515.</a>

## Installation

Install from PyPI:

```bash
pip install project-name
```

Or install from source:

```bash
git clone https://github.com/username/project-name.git
cd project-name
pip install -e .
```

## Quickstart

Minimal example showing the most common use case:

```python
from project_name import SomeClass

obj = SomeClass()
result = obj.do_something()
print(result)
```

## Basic Usage

Explain main modules/functions and short examples:

- project_name.module.function(args) — short description
- project_name.other.Class — short description

## Configuration

Describe configuration options, environment variables, or config files:

- CONFIG_OPTION — default: value — description

## CLI

If the package exposes a CLI:

```bash
project-name --help
project-name run --option value
```

## API Reference

Link to or list the main public API. Prefer linking to full docs if available.

- project_name.main_function(param1, param2) -> ReturnType
- project_name.Class.method(...) -> ReturnType

## Tests

Run tests locally:

```bash
pytest
```

## Contributing

Short contribution guidelines:

1. Fork the repo
2. Create a feature branch
3. Open a PR with tests and documentation
4. Follow the code style and commit message guidelines

## Changelog

Follow Semantic Versioning. Summaries of notable changes in each release (link to CHANGELOG.md).

## License

Specify license, e.g. MIT — see LICENSE file.

## Authors & Maintainers

- Name <email@example.com> — maintainer
- Contributor list in CONTRIBUTORS.md

## Support

Report issues at: https://github.com/username/project-name/issues

## Links

- PyPI: https://pypi.org/project/project-name
- Documentation: https://project-name.readthedocs.io (or docs folder)
- Source: https://github.com/username/project-name

Replace placeholders (project-name, username, links, examples) with real values.
