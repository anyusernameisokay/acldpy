
import numpy as np


###
# Build capital H
def calc_big_H(group_1_col, group_2_col, pvals, alpha):
    capital_H = list()
    for (group_1, group_2, p_value) in zip(group_1_col, group_2_col, pvals):
        if p_value < alpha:
            capital_H.append((group_1, group_2))
    return capital_H

def list_unique_groups(group_1_col, group_2_col):
    all_groups = group_1_col + group_2_col
    unique_groups = tuple(list(dict.fromkeys(all_groups))) # Ensure inmutable.
    return unique_groups


###
# Insert 
def insert_new_columns(M, i, j):    
    #IMPORTANT: I believe it is working, but needs checking.

    # Create a new matrix.
    new_matrix_columns = []
    idx_of_new_columns = []
    # Iterate over columns of M. (M.shape[1] is number of columns).
    for column_index in range(M.shape[1]):
        # Check whether column needs to be duplicated.
        column_in_M = M[:, column_index]
        ith_position = column_in_M[i]
        jth_position = column_in_M[j]

        # No insertion needed.
        if (ith_position == 1 and jth_position == 0) or (ith_position == 0 and jth_position == 1):
            new_matrix_columns.append(column_in_M)
            idx_of_new_columns.append(len(new_matrix_columns) - 1)

        # Column needs to be duplicated if it contains 1 on both, i and j.
        else:
            # One copy must be like M, with ith position 0, and jth position 1.
            # The other copy must be like M, with ith position 1, and jth position 0.
            column_copy_one = column_in_M.copy()
            column_copy_one.put([i, j], [0, 1])

            column_copy_two = column_in_M.copy()
            column_copy_two.put([i, j], [1, 0])

            new_matrix_columns.append(column_copy_one)
            new_matrix_columns.append(column_copy_two)

            # Index of newly added columns.
            idx_of_new_columns.append(len(new_matrix_columns) - 2)
            idx_of_new_columns.append(len(new_matrix_columns) - 1)
    return new_matrix_columns, idx_of_new_columns

###
# Absorb
def absorb_columns(M, idx_of_new_columns):
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
          
###
# Insert and absorb
def heuristic_insert_absorb(unique_groups, capital_H):
    i = 0 # For debugging.
    # FIXME: Naming ambigous!!! Change later. 
    # IMPORTANT: In here, we decided that the order of theunique groups is the order in the matrix.
    # 1) Generate inital treatment column.
    index_column = np.array(unique_groups) # Contains treatment. Also used to find row index.
    column_one = np.ones(len(unique_groups), dtype=np.int8).reshape(-1, 1) # One starts with a column of ones.
    M = column_one # Initial letter matrix.
    
    # 2) Iterate over significantly different pairs.
    for (group_one, group_two) in capital_H: # sig_dif = two groups that are significantly different
        # 2.1) Find indices of the groups that are significantly different.
        group_one_index = np.where(index_column == group_one)[0][0]
        group_two_index = np.where(index_column == group_two)[0][0]

        # 2.2) Insert and absorb.
        M, idx_of_new_columns = insert_new_columns(M, group_one_index, group_two_index)
        M = absorb_columns(M, idx_of_new_columns)

        # Reshape letter_matrix back to 2D array.
        M = np.array(M).T

        if i == 1:
            pass
        i += 1

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

### Calculate
# Still missing

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