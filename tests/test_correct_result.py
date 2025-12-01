from acld import run_cld, find_cld_columns
import pandas as pd
import pingouin as pg
from statsmodels.stats.multicomp import pairwise_tukeyhsd

TRUE_FEED_LETTER = {
    "sunflower": "a",    
    "casein": "a",    
    "meatmeal": "ab",   
    "soybean": "b",
    "linseed": "bc",
    "horsebean": "c",
}
def test_chickweights_example():
    chick_weights = pd.read_csv("tests/chick_weights.csv", sep=" ", skiprows=1)
    tk = pg.pairwise_tukey(chick_weights, dv="weight", between="feed")
    letter_order = ["sunflower", "casein", "meatmeal", "soybean", "linseed", "horsebean"]
    group_1_names, group_2_names, p_values = find_cld_columns(tk, "pg_tk")
    cld = run_cld(group_1_names, group_2_names, p_values, letter_order=letter_order)
    assert cld == TRUE_FEED_LETTER, "Test not passed!"



SAME_EXAMPLE_LETTER = {
    "treatment_1": "a",    
    "treatment_2": "a",
    "treatment_3": "a",
}
def test_same_example():
    group_1_names = ["treatment_1", "treatment_1", "treatment_2"]
    group_2_names = ["treatment_2", "treatment_3", "treatment_3"]
    p_values = [1, 1, 1]
    run_cld_result = run_cld(group_1_names, group_2_names, p_values)
    assert run_cld_result == SAME_EXAMPLE_LETTER, "Test not passed!"


DIFFERENT_EXAMPLE_LETTER = {
   "treatment_4": "a",
    "treatment_5": "b",
    "treatment_6": "c",
}
def test_different_example():
    group_1_names = ["treatment_4", "treatment_4", "treatment_5"]
    group_2_names = ["treatment_5", "treatment_6", "treatment_6"]
    p_values = [0.0, 0.0, 0.0]
    run_cld_result = run_cld(group_1_names, group_2_names, p_values, letter_order=["treatment_4", "treatment_5", "treatment_6"])
    assert run_cld_result == DIFFERENT_EXAMPLE_LETTER, "Test not passed!"


PENGUINS_LETTER = {
    "Adelie": "a",
    "Chinstrap": "a",
    "Gentoo": "b",
}
def test_penguin_ds():
    # 1) Using the penguin statistical library
    penguins = pg.read_dataset("penguins")
    penguins_tk_results = penguins.pairwise_tukey(dv='body_mass_g', between='species')
    group_1_col, group_2_col, pvals = find_cld_columns(penguins_tk_results, "pg_tk")
    final_letters = run_cld(group_1_col, group_2_col, pvals, letter_order=["Adelie", "Chinstrap", "Gentoo"])
    assert final_letters == PENGUINS_LETTER, "Test not passed!"

    # 2) Using statsmodels
    data = penguins[['body_mass_g', 'species']].dropna()
    statsmodels_tk_results = pairwise_tukeyhsd(data['body_mass_g'], data['species'])
    group_1_col, group_2_col, pvals = find_cld_columns(statsmodels_tk_results, "stm_tk")
    final_letters = run_cld(group_1_col, group_2_col, pvals, letter_order=["Adelie", "Chinstrap", "Gentoo"])
    assert final_letters == PENGUINS_LETTER, "Test not passed!"