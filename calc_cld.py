from typing import List, Tuple, Dict
import numpy as np

def calc_capital_h(
    group_1_col: List[str],
    group_2_col: List[str],
    p_vals: List[float],
    alpha: float
    ) -> List[Tuple[str, str]]:
    """
    Checks which treatment pairs are signficantly different from one another,
    based on whether respective p-value is smaller than signgicance level.
    
        Parameters: 
            group_1_col: List of all first elements to compare.
            group_2_col: List of all second elemnts to compare.
            p_vals: List of all p-values on which comparison is based on.
            alpha: Significance level. 
        
        Returns:
            capital_h: List of treatment pairs with significant difference.
    """
    capital_h = []
    for (group_1, group_2, p_value) in zip(group_1_col, group_2_col, p_vals):
        if p_value < alpha:
            capital_h.append((group_1, group_2))
    return capital_h

def list_unique_elements(
        group_1_col: List[str],
        group_2_col: List[str]
        ) -> Tuple:
    """
    List all elements that are included in the comparison.
    
        Parameters: 
            group_1_col: List of all first elements.
            group_2_col: List of all second elements.

        Returns:
            unique_elements: All unique elements.
    """
    all_groups = group_1_col + group_2_col
    unique_elements = tuple(list(dict.fromkeys(all_groups)))
    return unique_elements

def insert_new_columns(
        M: np.ndarray,
        i: np.ndarray,
        j: np.ndarray
        ) -> List[np.ndarray]:
    """
    Inserts new columns to the letter matrix if required. New columns are required for each
    original column that contains 1 in both rows that correspond to the two compared elements.
    In that case, the original column is removed, and  a two new ones are added: 
        1. Contains 1 in element row 1 and 0 in element row 2.
        2. Contains 0 in element row 1 and 1 in element row 2.
    This function is called once for each pair with significant difference.

        Parameters:
            M: Letter matrix as a 2D numpy array, where each column corresponds to an element (treatment),
                and each row corresponds to a letter (1 indicates presence of letter, 0 absence).
            i: Indices indicating for which letters the first element (treatment) has a 1.
            j: Indices indicating for which letters the second element (treatment) has a 1.

        Returns:
            new_matrix_columns: List of all columns after the insertion step.
    """
    new_matrix_columns = []

    # Iterate over columns of M. (M.shape[1] is number of columns).
    # And check whether column needs to be duplicated.
    for column_index in range(M.shape[1]):
        column_in_M = M[:, column_index]
        ith_position = column_in_M[i]
        jth_position = column_in_M[j]

        # No insertion needed, original column can be kept.
        if (ith_position == 1 and jth_position == 0) or (ith_position == 0 and jth_position == 1):
            new_matrix_columns.append(column_in_M)

        # Column needs to be duplicated if it contains 1 on both, i and j.
        else:
            # One copy must be like original, but with position 0, and jth position 1.
            # The other copy must be like original, but with position 1, and jth position 0.
            column_copy_one = column_in_M.copy()
            column_copy_one.put([i, j], [0, 1])

            column_copy_two = column_in_M.copy()
            column_copy_two.put([i, j], [1, 0])

            new_matrix_columns.append(column_copy_one)
            new_matrix_columns.append(column_copy_two)

    return new_matrix_columns

def absorb_columns(
        M: List[np.ndarray]
        ) -> List[np.ndarray]:
    """
    Absorbs columns, if possible. A column (each column is a letter) can be absorbed (= removed) if there exist another
    column that contains 1 for all the same elements (each row is an element).
    In the following example, L1 can be absorbed (removed), by L2.
       L1 L2 L3  
    T1 0  1  0
    T2 1  1  0
    T3 1  1  1
    T4 0  0  1
    
        Parameter:
            M: List of all columns after the insertion step.

        Returns:
            not_absorbed_cols: The letter matrix after absorbing columns.
    """

    not_absorbed_cols = [] # Collects all columns that need to be kept.
    # Tracks all cols that have been absobed.
    # Avoids 
    absorbed_cols_indices = []
    for col_one_id, col_one in enumerate(M):
        can_col_one_be_absorbed = False

        # Check each column.
        non_zero_col_one_idx = col_one.nonzero()
        # Compare against each other column
        for col_two_id, col_two in enumerate(M):
            # Skip comparison if cols are identical.
            if col_one_id == col_two_id:
                continue
            # Skip if col two has already been absorbed.
            elif col_two_id in absorbed_cols_indices: 
                continue
            # Otherwise do the comparison. 
            else: 
                non_zero_col_two_idx = col_two.nonzero()
                col_one_is_completly_in_col_two = np.in1d(non_zero_col_one_idx, non_zero_col_two_idx).all()
                if col_one_is_completly_in_col_two:
                    # Column one should not be kept.
                    absorbed_cols_indices.append(col_one_id)
                    can_col_one_be_absorbed = True
                    break
            
        # If we reach here, col one could not be absorbed.
        if not can_col_one_be_absorbed:
            not_absorbed_cols.append(col_one)

    return not_absorbed_cols
          
def insert_absorb(
        unique_elements: Tuple,
        capital_h: List[Tuple[int, int]]
        ) -> np.ndarray:
    """
    Iterates over the significantly different pairs,
    applying the insert-absorb algorithm to generate the letter matrix.

    Parameters:
        unique_elements: All unique elements.
        capital_h: List of treatment pairs with significant difference.

    Returns:
        M: Letter matrix as a 2D numpy array,
            where each column corresponds to an element (treatment),
            and each row corresponds to a letter (1 indicates presence of letter, 0 absence).
    """
    # 1) Generate inital treatment column.
    index_column = np.array(unique_elements)
    col_one = np.ones(len(unique_elements), dtype=np.int8).reshape(-1, 1) # Start with column of 1.
    M = col_one # Letter matrix.

    # 2) Iterate over significantly different pairs.
    for (group_one, group_two) in capital_h:
        # 2.1) Find indices of the groups that are significantly different.
        group_one_index = np.where(index_column == group_one)[0][0]
        group_two_index = np.where(index_column == group_two)[0][0]

        # 2.2) Insert and absorb.
        M = insert_new_columns(M, group_one_index, group_two_index)
        M = absorb_columns(M)

        # 2.3) Reshape letter_matrix back to 2D array.
        M = np.array(M).T
    return M

### 
# Sweep 
def sweep(M):
    # Go each letter (columns in the letter matrix)
    for first_column_nr, unique_letter_column in enumerate(M.T):
        # Go through each treatment in the column and check letter.
        for i_index, i_th_treat_let in enumerate(unique_letter_column):

            # If the letter is 0, nothing needs to be done.
            if i_th_treat_let == 0:
                continue
            # If the letter is 1, check whether it can be removed. (aka, replaced with 0)
            elif i_th_treat_let == 1:

                # Check for redundancy.
                # The ith letter can be changed in this first column from 1 to 0 if all 
                # other treatments (all jth) 
                # that share the letter with i.
                # also share another letter with i in another column
                jth_share_letter_with_ith = []

                # Go through the other treatments in the same column.
                for j_index, j_th_treat_let in enumerate(unique_letter_column):
                    # Skip if j_index is the same as i_index.
                    # Also skip if j_th_treat_let is 0.
                    if j_index == i_index or j_th_treat_let == 0:
                        continue
                    # If both, i_th_treat_let and j_th_treat_let are 1,
                    # Check if they have common letter in any other column.
                    ith_and_jth_pair_found_in_other_column = False
                    for second_column_nr, second_column in enumerate(M.T):
              
                        # Skip if second_column_nr is the same as first_column_nr.
                        if second_column_nr == first_column_nr:
                            continue
                        else:
                            # Check if both treatments have letter 1 in any second column.
                            if second_column[i_index] == 1 and second_column[j_index] == 1:
                                ith_and_jth_pair_found_in_other_column = True
                                break
                    jth_share_letter_with_ith.append(ith_and_jth_pair_found_in_other_column)
                # Check if all treatment-pairs i has a redundant letter in at least one other column with each j,
                ith_letter_in_first_column_redundant = all(jth_share_letter_with_ith)
                if ith_letter_in_first_column_redundant:
                    # Set the letter to 0.
                    M[i_index, first_column_nr] = 0

    # Remove empty columns (all zeros).
    non_empty_columns = []
    for column in M.T:
        if not np.all(column == 0):
            non_empty_columns.append(column)
    M = np.array(non_empty_columns).T


    # Return the swept matrix
    return M

### Determine letters

def determine_letters(letter_matrix, unique_groups, letter_type='low_a-z'):
    cld_dict = {}
    
    # How many letters a needed in total.
    n_letters = letter_matrix.shape[1]
    # Define which letters to use. (Doing it this way offers more flexibility later.)
    if letter_type == 'low_a-z':
        letters = [chr(i) for i in range(97, 97 + n_letters)]  # a-z
    elif letter_type == 'up_A-Z':
        letters = [chr(i) for i in range(65, 65 + n_letters)]  # A-Z
    else:
        raise ValueError("Not a valid letter type was chosen. Choose 'low_a-z' or 'up_A-Z'.")
    # Assign letters to groups.
    for i, group in enumerate(unique_groups):
        group_letters = ''
        for j in range(n_letters):
            if letter_matrix[i, j] == 1:
                group_letters += letters[j]
        cld_dict[group] = group_letters

    return cld_dict

def fill_all_zero_rows(letter_matrix):
    # Check for any all-0 rows
    zero_rows = np.all(letter_matrix == 0, axis=1)
    any_row_all_zero = np.any(zero_rows)
    if any_row_all_zero:
        # Create a new matrix with an additional column
        new_matrix = np.zeros((letter_matrix.shape[0], letter_matrix.shape[1] + 1), dtype=np.int8)
        # Copy the old matrix into the new one
        new_matrix[:, :-1] = letter_matrix
        # Set the last column to 1 for all-0 rows
        new_matrix[zero_rows, -1] = 1
        return new_matrix
    else:
        return letter_matrix

### Verify
def verify_cld(final_cld, group_one_column, group_two_column, p_values, alpha):
    for (group_one, group_two, p_value) in zip(group_one_column, group_two_column, p_values):
        letters_one = final_cld[group_one]
        letters_two = final_cld[group_two]

        # Check if there is any common letter between the two groups.
        shared_letters = set(letters_one).intersection(set(letters_two))

        if p_value <= alpha:
            # Groups should not share any letters.
            assert shared_letters == set(), f"Groups {group_one} and {group_two} share letters {shared_letters} but should not."
        else:
            # Groups should share at least one letter.
            assert shared_letters != set(), f"Groups {group_one} and {group_two} do not share any letters but should."
    return True

### Run the entire process
def run_clc(
    group_1_col: List[str],
    group_2_col: List[str],
    p_vals: List[float],
    alpha: float = 0.05,
    ) -> Dict[str, str]:
    """
    Computes a Compact Letter Display (CLD) from pairwise group comparisons.
    Implements the insert-absorb and sweep algorithms by Piepho (2004).
    First, all significant differences between element pairs are identified.
    Then, the insert-absorb and sweep algorithms are applied to find a clc with minimal letters.
    Finally, the letter assignment is verified against the original pairwise comparisons.

        Parameters: 
            group_1_col: List of all first elements to compare.
            group_2_col: List of all second elements to compare.
            p_vals: List of all p-values on which comparison is based on.
            alpha: Significance level. 
        
        Returns: 
            final_letters: Dictionary mapping each element to its assigned letters.
    """
    # 1) Filter out all pairs with significant differences (capital_h).
    capital_h = calc_capital_h(group_1_col, group_2_col, p_vals, alpha)
    # 2) List all unique elements.
    unique_elements = list_unique_elements(group_1_col, group_2_col)
    # 3) Insert and absorb algorithm.
    letter_matrix = insert_absorb(unique_elements, capital_h)
    # 4) Sweep
    letter_matrix = sweep(letter_matrix)
    # Fill in any all-0 rows
    letter_matrix = fill_all_zero_rows(letter_matrix)
    # 5) Translate matrix into letters.
    final_letters = determine_letters(letter_matrix, unique_elements)
    # 6) Verify that the calculated solutions solves the problem correctly.
    verify_cld(final_letters, group_1_col, group_2_col, p_vals, alpha)

    return final_letters