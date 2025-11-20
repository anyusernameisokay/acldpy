# acld

[![PyPI](https://img.shields.io/pypi/v/project-name.svg)](https://pypi.org/project/project-name)
[![Python](https://img.shields.io/pypi/pyversions/project-name.svg)]()
[![License](https://img.shields.io/pypi/l/project-name.svg)]()

## Summary

This Python 3 package assigns letters to indicate statistically significant
differences between groups following pairwise comparisons. It strives to be
compatiple with all major Python statistics librairies.

<strong>acld = agnostic compact letter display</strong>

Users conduct their statistical test with the library of their choice. Then,
they pass their result to run_cld.
The package implements algorithms that were described by Piepho
and coworkers [1,2].

## Installation

Install from PyPI:

```bash
pip install acld
```

## Basic usage

To calculate the cld, you need three arguments.

1. List of all first group names used in the pairwise comparisons.
2. List of all second group names used in the pairwise comparisons.
3. A list of the p-values associated with each comparison.

<strong>Generally</strong>, one's input should follow this structure: ith element of `p-values` corresponds to the p-value for the comparison between the ith entry in `group_1_names` and the i-th entry in `group_2_names`:

```python
group_1_names = ["element 1", "element 1", "element 2"]
group_2_names = ["element 2", "element 3", "element 3"]
p_values = [0.9, 0.2, 0.01]
```

These three lists are passed to the the `run_clc` function of the acld library. `run_clc` returns a dictionary where each key is a unique element and the value are its associated letter.

```python
from acld import run_clc

cld = run_clc(group_1_col, group_2_col, p_values)
print (cld) # {'element 1': 'ab', 'element 2': 'b', 'element 3': 'a'}
```

<strong>Typically</strong>, the these three required lists can be parsed from the returned object of a stastical test, as illustrated here with the Pingouin implementation of the Tukey-Kramer test.

```python
import pingouin as pg
from acld import run_clc

penguins = pg.read_dataset("penguins") # Example dataset
tk_result = penguins.pairwise_tukey(dv='body_mass_g', between='species')
group_1_names, group_2_names, p_values = list(tk_result["A"]), list(tk_result["B"]), list(tk_result["p-tukey"])

cld = run_clc(group_1_names, group_2_names, p_values)
print (cld) # {'Adelie': 'b', 'Chinstrap': 'b', 'Gentoo': 'a'}
```

Besides these three lists, `run_clc` accepts two optional arguments:

1. `alpha` (float, default: 0.05): Significance level. Two elements are considered significantly different if their p‑value is less ("<", not "=<"!) than alpha.
2. `letter_order` (None | list, default: None): If set, a list containing all elements in the order of which they should be assigned letters. Often, one would like to assign the letters in ascending order of the element mean values.

```python
from acld import run_clc

group_1_names = ["element 1", "element 1", "element 1", "element 2", "element 2", "element 3"]
group_2_names = ["element 2", "element 3", "element 4", "element 3", "element 4", "element 4"]
p_values = [0.08, 0.02, 0.01, 0.2, 0.04, 0.08]
mean_values = {"element 1": 1.2, "element 2": 2.8, "element 3": 3.2, "element 4": 4.0}

cld = run_clc(group_1_names, group_2_names, p_values) # default values for alpha and letter_order
print(cld) # {'element 1': 'c', 'element 2': 'bc', 'element 3': 'ab', 'element 4': 'a'}

mean_values_sorted = dict(sorted(mean_values.items(), key=lambda item: item[1]))
cld = run_clc(group_1_names, group_2_names, p_values, alpha=0.1, letter_order=mean_values_sorted.keys())
print(cld) # {'element 1': 'a', 'element 2': 'b', 'element 3': 'b', 'element 4': 'c'}
```

## Extra Functionality

`find_cld_columns` is a helper function that accepts the result objects of the most common statistical tests and returns the three required lists.

```python
from acld import find_cld_columns

group_1_names, group_2_names, p_values = find_cld_columns(penguins_tk_results, "pg_tk")
```

Currently it works with the output of the following tests:

1. `result_type="pg_tk"`: <a href="https://pingouin-stats.org/build/html/generated/pingouin.pairwise_tukey.html#pingouin-pairwise-tukey">pingouin's Tukey-Kramer test</a>
2. `result_type="stm_tk"`: <a href="https://www.statsmodels.org/dev/generated/statsmodels.sandbox.stats.multicomp.MultiComparison.tukeyhsd.html#statsmodels-sandbox-stats-multicomp-multicomparison-tukeyhsd">statsmodel's Tukey-Kramer test</a>

## Development & Planned Features

The project is in its early development.
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
