
# {{{ File Information }}} --------------------------------------------------------------------------------------------------------------------------------------------------------


# - Name: launcher.py
# - Author(s): Andrew Gillett (R10797)
# - Last Modified: 28.04.2024 : 11:43:09
# - File Version: 1.0

# - Description: The primary purpose of this program is to navigate through a set
#                directory structure containing Python files and execute them or
#                specific functions within them.


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# {{{ Import Libraries }}} --------------------------------------------------------------------------------------------------------------------------------------------------------


import os           # For interacting with the operating system
import subprocess   # For spawning new processes, used here to execute Python files
import pyfiglet     # For generating ASCII art text
import ast          # For parsing Python code into abstract syntax trees, used to extract function names


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# {{{ ANSI Formatting Escape Codes }}} --------------------------------------------------------------------------------------------------------------------------------------------


reset = "\033[0m"          # ANSI escape code to reset text formatting

bold = "\033[1m"           # ANSI escape code for bold text
underline = "\033[4m"      # ANSI escape code for underlined text

darkRed = "\033[31m"       # ANSI escape code for dark red text
darkGreen = "\033[32m"     # ANSI escape code for dark green text
darkYellow = "\033[33m"    # ANSI escape code for dark yellow text
darkBlue = "\033[34m"      # ANSI escape code for dark blue text

purple = "\033[35m"        # ANSI escape code for purple text
pink = "\033[95m"          # ANSI escape code for pink text

cyanHighlight = "\033[46m" # ANSI escape code for cyan highlight


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# {{{ Common Functions }}} --------------------------------------------------------------------------------------------------------------------------------------------------------


# [FUNCTION] Clear the Terminal
# - Clears the terminal using the os package
def clear_terminal():
    # Comment/Uncomment Accordingly!
    os.system('clear') # For Unix-based systems
    # os.system('cls') # For Windows-based systems


# [FUNCTION] Display the Running/Ended Processes
# - Display the currently running and ended processes depending if the "stage" is "start" or "end"
def announce_execution(stage, type, filePath):
    if stage == "start":
      
      if type == "file":
        print(f"\n{bold}{darkRed}▶ Now Running: {os.path.basename(filePath)}{reset}\n")
        
      else:
        print(f"\n{bold}{darkRed}▶ Now Running: {type} in {os.path.basename(filePath)}{reset}\n")
        
    elif stage == "end":
      
      if type == "file":
        print(f"{bold}{darkGreen}\n▶ Successfully Executed: {os.path.basename(filePath)}{reset}")

      else:
        print(f"{bold}{darkGreen}\n▶ Successfully Executed: {type} in {os.path.basename(filePath)}{reset}")


# [FUNCTION] Print the Welcome Message
def welcome_message():
    clear_terminal() # Clear the terminal
  
    pyfigletObject = pyfiglet.Figlet().renderText(title)  # Generate ASCII art text of the 'title'
    print(f"{titleArt}{pyfigletObject}{reset}")  # Print the ASCII art text with ANSI formatting
    print(f"{descriptionArt}{description}{reset}\n")  # Print the description with ANSI formatting


# [FUNCTION] Extract Functions
# - This function parses a Python file and extracts functions that start with #_.
def get_functions_from_file(filePath):
    functions = []  # List to store function names
  
    with open(filePath, 'r') as file:
        tree = ast.parse(file.read())  # Parse the Python code into an abstract syntax tree
      
        for node in ast.walk(tree):
          
            if isinstance(node, ast.FunctionDef) and node.name.startswith(functionPrefix):  # Check if function starts with [characters]
                functions.append(node.name)  # Add the function name to the list
              
    if not functions:
        return None  # Return None if no functions found
      
    return functions  # Return the list of functions


# [FUNCTION] Execute Another Python file
# - This function executes another Python file using subprocess.run().
def run_another_file(filePath):
    announce_execution("start", "file", filePath)  # Print message indicating the start of execution
    try:
        subprocess.run(['python', filePath], check=True)  # Run the Python file using subprocess
        announce_execution("end", "file", filePath)  # Print message indicating the successful execution
    except subprocess.CalledProcessError as e:
        print(f"Error running {filePath}: {e}")  # Print error message if execution fails


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# {{{ Error Handling }}} ----------------------------------------------------------------------------------------------------------------------------------------------------------
# - Functions which output an error message


# Selection value is not valid
def error_invalid_input():
  print(f"{bold}Invalid input. Please enter a valid number{reset}")  # Print error message for invalid input
  input(f"{pink}Continue?: {reset}")  # Prompt for continuation

  
# File is not a Python file
def error_unsuported_item():
  print("Unable to execute due to item being unsupported.")  # Print error message for unsupported file type
  input(f"{pink}Continue?: {reset}")  # Prompt for continuation

  
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# {{{ Main Program }}} ------------------------------------------------------------------------------------------------------------------------------------------------------------
# - These are the main components and functionalities of the program.


# [FUNCTION] Navigate the Chosen Directory and Execute Selected Python Files/Their Functions
def navigate_directory(directory):
    while True: # (Until Stopped)

        # Initialise empty lists for 'subfolders' and 'files'
        subfolders, files = [], [] 

        # Iterate through the directory
        for item in os.listdir(directory):

            # Check if the item is a directory
            if os.path.isdir(os.path.join(directory, item)) and item != "__pycache__":
                subfolders.append(item)  # Add subfolder name to subfolders list

            else:
                files.append(item)  # Add file name to files list

        welcome_message()  # Display the welcome message

        if directory != startingDirectory:
            print(f"{bold}{darkRed}0: <- Go Back{reset}")  # Print option to go back to the parent directory

        subfolders.sort()  # Sort subfolders alphabetically
        files.sort()  # Sort files alphabetically

        # Print subfolder options
        for i, subfolder in enumerate(subfolders):
            print(f"{i + 1}: [Subfolder] {subfolder}")  # Print subfolder options

        # Print file options
        for i, file in enumerate(files):
          
            if file.endswith('.py'):  # Check if it's a Python file
                print(f"{len(subfolders) + i + 1}: {cyanHighlight}[File] {file}{reset}")  # Print files with cyan highlight
              
            else: # Files must not be python files
                print(f"{len(subfolders) + i + 1}: [File] {file}")  # Print file options

        # Prompt for user input
        choice = input(f"\n{darkBlue}Enter the number of a subfolder or file (-1 to exit, # to clear): {reset}")

        # If statement that determines the outcome depending on the user's input of 'choice'
        if choice == "-1": # If the choice is "-1":
            break          # Exit the loop - effectively ending the program

        elif choice == "0" and directory != startingDirectory: # Elseif the choice is "0" and the directory is not the starting directory:
            directory = os.path.dirname(directory)             # Move to the parent directory if user chooses to go back

        elif choice == "#":  # Elseif the choice is "#":
            clear_terminal() # Clear the terminal if user chooses to clear

        else: # If no other parameter is met (a subfolder/file is selected):
            try:

                choice = int(choice)  # Convert user input to integer

                # If user chooses a subfolder:
                if 1 <= choice <= len(subfolders): 

                    directory = os.path.join(directory, subfolders[choice - 1])  # Set the new directory path

                # Elseif user chooses a file:
                elif len(subfolders) < choice <= len(subfolders) + len(files):

                    fileIndex = choice - len(subfolders) - 1  # Calculate index of the chosen file

                    # If the file index is valid:
                    if 0 <= fileIndex < len(files):

                        fileToExecute = os.path.join(directory, files[fileIndex])  # Get the full path of the chosen file

                        # If the file path corresponds with a file
                        if os.path.isfile(fileToExecute):

                            # If the file is a Python file:
                            if fileToExecute.endswith('.py'):
                              
                                functions = get_functions_from_file(fileToExecute)  # Get functions from the file

                                if functions:  # If there are functions in the file:

                                    welcome_message()  # Display welcome message

                                    # Menu Heading: 'Functions in file: [file]'
                                    print(f"\n{bold}{darkYellow}Functions in file: {reset}{os.path.basename(fileToExecute)}{reset}")
                                    # Option 0: 'Go Back' to previous directory
                                    print(f"{darkRed}0: <- Go Back{reset}")

                                    # Iterate for every function in the file
                                    for i, function in enumerate(functions):
                                        print(f"{i + 1}: {function[2:]}")  # Print function options

                                    # Prompt for user input
                                    functionChoice = input(f"\n{darkBlue}Enter the number of the function to run (0 to cancel, # to clear): {reset}")  # Prompt for function choice

                                    # If user input is "0":
                                    if functionChoice == "0":
                                        continue  # Continue to next iteration if user cancels

                                    try:

                                        if functionChoice == "#":
                                            clear_terminal()  # Clear the terminal

                                        else:

                                            functionChoice = int(functionChoice)  # Convert function choice to integer

                                          
                                            # If function choice is valid:
                                            if 1 <= functionChoice <= len(functions): 
                                                clear_terminal()  # Clear the terminal
                                              
                                                exec(open(fileToExecute).read())  # Execute the file
                                                selectedFunction = functions[functionChoice - 1]  # Get the selected function
                                              
                                                announce_execution("start", f"'{selectedFunction[2:]}'", fileToExecute) # Announce the start of execution
                                                eval(selectedFunction)()                                                # Execute the selected function
                                                announce_execution("end", f"'{selectedFunction[2:]}'", fileToExecute)   # Announce the end of execution
                                              
                                                input("\nPress Enter to continue...")  # Wait for user input

                                            else:
                                                error_invalid_input()

                                    except (ValueError, SyntaxError, TypeError):
                                        error_invalid_input()

                                else: # Run the entire python file if no functions are found
                                      clear_terminal()  # Clear the terminal
                                      run_another_file(fileToExecute)  # Execute the file
                                      input(f"{pink}Continue?: {reset}")  # Prompt for continuation
                                  
                            else:
                                error_unsuported_item()
                              
                        else:
                            error_unsuported_item()

                    else:
                        error_invalid_input()

                else:
                    error_invalid_input()

            except ValueError:
                error_invalid_input()


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  
# {{{ Program Execution }}} -------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
  
    # Directory and Function Identifier Formatting
    startingDirectory = "."  # Set the starting directory to the current directory
    functionPrefix = "__"    # Set the function identifier as those with the selected prefix

    # Title and Description Formatting
    title = "Mother Lies"  # Set the launcher title
    titleArt = f"{bold}{purple}"  # Set the formatting for the title
    description = "Directory Navigator and Python Executor:"  # Set the description
    descriptionArt = f"{underline}{darkGreen}"  # Set the formatting for the description

    navigate_directory(startingDirectory)  # Call the 'navigate_directory' function to start the program


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

