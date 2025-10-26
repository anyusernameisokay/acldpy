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
The package implements algorithms that were described by Piepho
and coworkers [1,2].

## Installation

Install from PyPI:

```bash
pip install acld
```

## Basic usage
We first conduct a statistical compairison with the library of our choice. 
Then, we pass the result to the acld function. 
```python
from acld import run_cld

obj = SomeClass()
result = obj.do_something()
print(result)
```


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
<br><br>
I am not affiliated with the authors of these studies. 


## License

Specify license, e.g. MIT — see LICENSE file.

## Authors & Maintainers

- Name <email@example.com> — maintainer
- Contributor list in CONTRIBUTORS.md

## Support

Report issues at: https://github.com/username/project-name/issues

## Links

- PyPI: https://pypi.org/project/project-name
- Source: https://github.com/username/project-name

Replace placeholders (project-name, username, links, examples) with real values.
