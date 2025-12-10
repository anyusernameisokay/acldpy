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
        group_2_col: List[str],
        letter_order: None | List[str],
        ) -> Tuple:
    """
    List all elements that are included in the comparison. If an order
    is given, the elements are put in that order and it is checked 
    whether unique elements  (derived from the groups) and the list of 
    ordered elements are the same.
    
        Parameters: 
            group_1_col: List of all first elements.
            group_2_col: List of all second elements.
            letter_order: XXX.
        Returns:
            unique_elements: All unique elements.
    """
    all_groups = group_1_col + group_2_col
    unique_elements = tuple(list(dict.fromkeys(all_groups)))
    if isinstance(letter_order, list):
        assert sorted(unique_elements) == sorted(letter_order), f"""The provided order must contain all the same elements found in the element groups.
        Provided order contains {letter_order}
        Elements found in groups are: {unique_elements}
        """
        unique_elements = tuple(letter_order)

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

        # IMPORTANT: Check whether this is true 
        elif ith_position == 0 and jth_position == 0:
            new_matrix_columns.append(column_in_M)

        # Column needs to be duplicated if it contains 1 on both, i and j.
        elif ith_position == 1 and jth_position == 1:
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
            not_absorbed_cols: The letter matrix containing only columns that could not be absorbed.
    """
    # Collects all columns that need to be kept.
    not_absorbed_cols = []

    # Tracks cols that have been absobed to avoid columns reffering to each
    # other when determing whether they should be absorbed.
    absorbed_cols_indices = [] 

    for col_one_id, col_one in enumerate(M):
        can_col_one_be_absorbed = False
        non_zero_col_one_idx = col_one.nonzero()
        # Compare against each other column
        for col_two_id, col_two in enumerate(M):
            # Skip comparison if cols are identical.
            if col_one_id == col_two_id:
                continue
            # Skip if col two has already been absorbed.
            elif col_two_id in absorbed_cols_indices: 
                continue
            # Otherwise check whether absorbance is possible.
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

def sweep(
        M: np.ndarray
        ) -> np.ndarray:
    """
    Performs sweeping of the matrix that is derived from the insert-absort algorithm. A column can
    be removed if for each possible pair of rows containing 1s, there is at least one other column 
    that contains 1s for in the same row. In the following example column L2 can be removed via sweeping.
      L1 L2 L3  L4
    T1 1  1  0  1
    T2 1  0  0  1
    T3 1  1  1  0
    T4 0  0  1  0
    T5 0  1  1  1

        Parameter:
            M: 2D letter matrix, after insert-absorb.

        Returns:
            M: 2D letter matrix, after sweep
    """
    # Iterate over letters (columns in the letter matrix)
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
                # other treatments (all jth) that share the letter with i,
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
                # Check if all pairs between i and any j, share a letter in at least one column.
                # if jth_share_letter_with_ith is empty, it means that i_th_treat_let was the only one with letter 1 in this column.
                # In that case, it wether it can be removed or not, depends on whether the treatment has any other 1 in its row.

                # TODO: Check: whether the logic here makes sense. Esentially, we want ot remove the lettter accoring to the rules above.
                # However, if the letter is alone, because there is no other letter in the columnn, we can remove it regardless. 
                # However, ONLY, if , after removing, we still have at least one letter for the treatment (same row, other column)!!! This code needs to be checked.
                ith_letter_is_only_letter_in_ith_row = np.sum(M[i_index, :]) == 1
                ith_letter_connected_to_all_jths_in_other_cols = all(jth_share_letter_with_ith) and len(jth_share_letter_with_ith) > 0 # Name is misleading.
                
                if ith_letter_connected_to_all_jths_in_other_cols: 
                    M[i_index, first_column_nr] = 0
                if not ith_letter_is_only_letter_in_ith_row and len(jth_share_letter_with_ith) == 0:
                    M[i_index, first_column_nr] = 0
                

    # Remove empty columns (all zeros).
    non_empty_columns = []
    for column in M.T:
        if not np.all(column == 0):
            non_empty_columns.append(column)
    M = np.array(non_empty_columns).T

    return M

def determine_letters(
        letter_matrix: np.ndarray,
        unique_groups: Tuple,
        letter_type: str ='low_a-z'
        ) -> Dict[str, str]:
    """
    Translates the letter matrix into a dictionary mapping each element to its assigned letters.
        Parameters:
            letter_matrix: 2D letter matrix after sweep and sorting (optional).
            unique_groups: All unique elements.
            letter_type: Type of letters to use. 'low_a-z' for lowercase letters, 'up_A-Z' for uppercase letters.
        
        Returns:
            cld_dict: Dictionary mapping each element to its assigned letters.
    """
    cld_dict = {}
    
    n_letters = letter_matrix.shape[1]
    if letter_type == 'low_a-z':
        letters = [chr(i) for i in range(97, 97 + n_letters)]  # a-z
    elif letter_type == 'up_A-Z':
        letters = [chr(i) for i in range(65, 65 + n_letters)]  # A-Z
    else:
        raise ValueError("Not a valid letter type was chosen. Choose 'low_a-z' or 'up_A-Z'.")
    
    for i, group in enumerate(unique_groups):
        group_letters = ''
        for j in range(n_letters):
            if letter_matrix[i, j] == 1:
                group_letters += letters[j]
        cld_dict[group] = group_letters

    return cld_dict

def fill_all_zero_rows(letter_matrix: np.ndarray) -> np.ndarray:
    """
    Fills in any all-0 rows in the letter matrix by adding an additional column.
    The new column will have a 1 in the positions of the all-0 rows, and 0s elsewhere.
    This is necessary as the insert-absorb and sweep minimize use of letters, but the 
    subseuent translation to letters requires that each element has at least one letter.

        Parameter:
            letter_matrix: 2D letter matrix after sweep.

        Returns:
            Either: Original letter matrix if no all-0 rows were found.
            Or: Letter matrix after adding column for all-0 rows.
    """
    # Check for any all-0 rows
    print(letter_matrix)
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

def sort_letters(
        M: np.ndarray
        ) -> np.ndarray:
    # IMPORTANT: CHECK!
    """
    Sorts the columns of a binary letter matrix by prioritizing columns with 1s in higher rows.

    Columns are ordered left to right based on the earliest occurrence of a 1 in each column:
        - Columns with a 1 in the first row are placed furthest to the left.
        - If multiple columns have a 1 in the same row, the next row is used to break the tie.
        - This process continues row by row until all columns are uniquely ordered.

       L1 L2 L3         L1 L2 L3       
    T1 0  1  0        T1 1  0  0  
    T2 1  1  0   -->  T2 1  1  0  
    T3 1  1  1        T3 1  1  1  
    T4 0  0  1        T4 0  0  1    

        Parameter:
            M: Unsorted letter matrix.

        Returns
            sorted_M: Matrix after the sorting algorithm.
    """
    sorted_indices = np.lexsort(M[::-1, :])
    sorted_indices =np.flip(sorted_indices)
    sorted_M = M[:, sorted_indices]

    return sorted_M

def verify_cld(final_letters, group_1_col, group_2_col, p_vals, alpha):
    """
    Checks whether the calculated cld is accurate by checking that elements, that are siginicantly
    different share no letter, and elements that are not significantly different share at least 
    one letter in the final cld. An exception is thrown, if are mistake is discovered.

        Parameters:
            final_letters:
            group_1_col: List of all first elements to compare.
            group_2_col: List of all second elements to compare.
            p_vals: List of all p-values on which comparison is based on.
            alpha: Significance level. 

        Returns nothing.
    """
    for (group_one, group_two, p_value) in zip(group_1_col, group_2_col, p_vals):
        letters_one = final_letters[group_one]
        letters_two = final_letters[group_two]

        # Check if there is any common letter between the two groups.
        shared_letters = set(letters_one).intersection(set(letters_two))

        if p_value < alpha:
            # Groups should not share any letters.
            assert shared_letters == set(), f"Groups {group_one} and {group_two} share letters {shared_letters} but should not."
        else:
            # Groups should share at least one letter.
            assert shared_letters != set(), f"Groups {group_one} and {group_two} do not share any letters but should."
    return

### Run the entire process
def run_cld(
    group_1_col: List[str],
    group_2_col: List[str],
    p_vals: List[float],
    alpha: float = 0.05,
    letter_order: None | List[str] = None,
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
            letter_order: Optional. List of all elements in the order they should get assigned 
                           letters. The first element in the list will get the "lowest" letter.
        
        Returns: 
            final_letters: Dictionary mapping each element to its assigned letters.
    """
    # 1) Filter out all pairs with significant differences (capital_h).
    capital_h = calc_capital_h(group_1_col, group_2_col, p_vals, alpha)
    # 2) List all unique elements.
    unique_elements = list_unique_elements(group_1_col, group_2_col, letter_order)
    # 3) Insert and absorb algorithm.
    letter_matrix = insert_absorb(unique_elements, capital_h)
    print("letter matrix after insert-absorb")
    print(letter_matrix)
    if DEBUG and TEST_PERMUT:
        letter_matrix = rearrange_columns(letter_matrix)
    # 4) Sweep
    letter_matrix = sweep(letter_matrix)
    print("letter matrix after Sweep")
    print(letter_matrix)
    # 5) Fill in any all-0 rows
    letter_matrix = fill_all_zero_rows(letter_matrix)
    # 6) Sort letter matrix rows according to unique elements order.
    letter_matrix = letter_matrix if isinstance(letter_order, type(None)) else sort_letters(letter_matrix)

    # 7) Translate matrix into letters.
    final_letters = determine_letters(letter_matrix, unique_elements)
    # 8) Verify that the calculated solutions solves the problem correctly.
    verify_cld(final_letters, group_1_col, group_2_col, p_vals, alpha)

    return final_letters

DEBUG = False
TEST_PERMUT = False
"""
def rearrange_columns(M):
    # Not used yet....
    print("Before permutation")
    print(M)
    perm_one = [4,3,2,1,0,5]

    idx = np.empty_like(perm_one)
    idx[perm_one] = np.arange(len(perm_one))
    M[:, idx]
    M[:] = M[:, idx] 
    print("After permutation")
    print(M)
    return M

# Debugging

if __name__ == "__main__":
    DEBUG = True
    if DEBUG:
        
        group_1_names = ["T1"] * 7 + ["T2"] * 6 + ["T3"] * 5 + ["T4"] * 4 + ["T5"] * 3 + ["T6"] * 2 + ["T7"] * 1 + ["T8"] * 0
        group_2_names = []
        for t in range(1, 9):
            for t2 in range(t + 1, 9):
                group_2_names.append(f"T{t2}")
        print(group_1_names)
        print(group_2_names)
        p_values = [1] * len(group_1_names)
        sig_dif_pairs = [["T1", "T7"], ["T1", "T8"], ["T2", "T4"], ["T2", "T5"], ["T3", "T5"]]
        for t1, t2 in sig_dif_pairs:
            for p_id in range(len(p_values)):
                if (group_1_names[p_id] == t1) and (group_2_names[p_id] == t2):
                    print(t1, t2)
                    p_values[p_id] = 0
        
        final_letters = run_cld(group_1_names, group_2_names, p_values,)
        print(final_letters)

"""