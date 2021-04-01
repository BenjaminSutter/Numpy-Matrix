"""
Name: Ben Sutter
Date: November 3rd, 2020
Class: SDEV 300
Purpose: Parses phone numbers and zip codes. Also prompts the user to make a 3x3 matrix.
The user then can select various calculations to perform on the matrix.
"""

import sys
import numpy as np


def matrix_to_string(matrix):
    """Displays matrix without brackets.
    Code for function found from https://stackoverflow.com/a/9829993"""
    return '\n'.join(' '.join(str(cell) for cell in row) for row in matrix)


def int_check(incoming_list):
    """This function is isdigit() for a list (checks each element to see if it is an int).
    pandas.is_integer_dtype didn't work how I thought, or perhaps I wasn't using it correctly."""
    ints = 0  # Keeps track of how many ints were found
    for _, item in enumerate(incoming_list):
        if item.isdigit():  # If it is a digit, increase the int count
            ints += 1
    # If found ints equals the length of the list (all contents are ints), then return true
    if ints == len(incoming_list):
        return True
    return False


def matrix_check(message):
    """Preforms various checks to make sure the matrix is 3x3, and returns matrix after checks.
    It checks each row as it is entered so if an invalid row is entered it tells the user."""
    print(message)  # Prints the message passed as a parameter, message is never used again
    matrix_array = []  # Will be added to as correct input occurs
    for i in range(3):  # Loop runs 3 times (3 rows)
        incoming = input("")  # Blank line for input
        row = incoming.split()  # Split the input into an array (divider is spaces)
        while True:
            # If it contains 3 variables and all are ints, then typecast variables to new list
            if len(row) == 3 and int_check(row):
                int_row = [int(row[0]), int(row[1]), int(row[2])]
                break
            # If not true, then give user new input and show which row is wrong
            incoming = input("Invalid row #" + str(i + 1) +
                             "\nInput must be 3 integers separated by spaces"" (x y z). "
                             "Please try again:\n")
            row = incoming.split()  # Reset the value of row so user can try again
        # If while loop is broken, then add the valid int_row to matrix_array
        matrix_array.append(int_row)
    return matrix_array  # Return the array so it can be can be converted using np.array


def matrix_results(matrix):
    """Prints the transposed matrix, and shows mean of columns and rows of transposed matrix"""
    transposed = matrix.transpose()
    print("The transpose is:\n" + matrix_to_string(transposed))
    row = []
    column = []
    # Used to make formatting look more clean
    for i in range(3):
        row_mean = matrix.mean(axis=1)[i]
        # If the i variable is integer then typecast and add
        if row_mean.is_integer():
            row.append(int(row_mean))
        else:  # If not in then round to two places and append
            row.append(round(row_mean, 2))

        column_mean = matrix.mean(axis=0)[i]
        # If the i variable is integer then typecast and add
        if column_mean.is_integer():
            column.append(int(column_mean))
        else:  # If not in then round to two places and append
            column.append(round(column_mean, 2))
    print("\nThe row and column mean values of the results are:"
          "\nRow: " + str(row) + "\nColumn: " + str(column))

# Store prompt for starting the "game"
PLAY_CHECK = "\nDo you want to play the Matrix Game? (Yes/No)\n"

# Store prompt for matrix operation selection"
OPERATION_OPTIONS = ("\nSelect a Matrix Operation from the list below:"
                     "\na. Addition"
                     "\nb. Subtraction"
                     "\nc. Matrix multiplication"
                     "\nd. Element by element multiplication\n")

user_selection = input("Welcome to the program!" + PLAY_CHECK)
while user_selection.upper() != "NO":

    # While selection is invalid, give user prompt to make the selection valid
    while user_selection.upper() != "YES" and user_selection.upper() != "NO":
        user_selection = input("Please select a valid option (Yes/No): ")

    if user_selection.upper() == "YES":

        phone_num = input("Enter your phone number (XXX-XXX-XXXX:)\n")
        # While the criteria that determines the phone number format is not met, then loop
        while True:
            # phone_num[:3] = area code, phone_num[4:7] = exchange code, phone_num[8:12] = last four
            # Check if the sum of their string (aka they are all numbers) is a digit
            # Length should also be 12, 4th and 8th characters should be "-"
            if ((phone_num[:3] + phone_num[4:7] + phone_num[8:12]).isdigit() and len(
                    phone_num) == 12 and phone_num[3] == "-" and phone_num[7] == "-"):
                break
            phone_num = input("Your phone number is not in correct format. Please renter: ")

        zip_code = input("Enter your zip code+4 (XXXXX-XXXX):\n")
        # While the criteria that determines the zip-code format is not met, then loop
        while True:
            if (len(zip_code) == 10 and zip_code[:5].isdigit()
                    and zip_code[6:10].isdigit() and zip_code[5] == "-"):
                break
            zip_code = input("Your zip code is not in correct format. Please renter: ")

        # Creates the first and second matrices based on user input
        first_matrix = np.array(matrix_check("Enter your first 3x3 matrix:"))
        second_matrix = np.array(matrix_check("Enter your second 3x3 matrix:"))
        # Prints the information about the matrices
        print("Your first matrix is: \n" + matrix_to_string(first_matrix) +
              "\nYour second matrix is: \n" + matrix_to_string(second_matrix))

        operation_choice = input(OPERATION_OPTIONS)  # Determines matrix operation selection
        # While selection is invalid, loop til user puts valid selection
        while operation_choice.lower() not in ("a", "b", "c", "d"):
            operation_choice = input("Please select a valid option (a, b, c, or d): ")

        if operation_choice.lower() == "a":
            addition = first_matrix + second_matrix  # Creates matrix from sum
            print("You selected addition. The results are: \n" + matrix_to_string(addition))
            matrix_results(addition)  # Shows transpose, then mean of column and rows

        elif operation_choice.lower() == "b":
            subtraction = first_matrix - second_matrix  # Creates matrix from subtraction
            print("You selected subtraction. The results are: \n" + matrix_to_string(subtraction))
            matrix_results(subtraction)  # Shows transpose, then mean of column and rows

        elif operation_choice.lower() == "c":
            multiplication = np.matmul(first_matrix, second_matrix)  # Creates matrix from matmul
            print("You selected matrix multiplication. "
                  "The results are: \n" + matrix_to_string(multiplication))
            matrix_results(multiplication)  # Shows transpose, then mean of column and rows

        elif operation_choice.lower() == "d":
            element = first_matrix * second_matrix  # Creates matrix from element multiplication
            print("You selected element by element multiplication. "
                  "The results are: \n" + matrix_to_string(element))
            matrix_results(element)  # Shows transpose, then mean of column and rows

    # End of selection, so if current user_selection is not no (quit) then let user choose again
    if user_selection.upper() != "NO":
        user_selection = input(PLAY_CHECK)

# The while loop has ended because option 5 was selected so thank the user and exit
print("Thank you for using the program, have a nice day!")
sys.exit()
