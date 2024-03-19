# DSPY_VBWyrde
DSPY Experiments

This is intended to be a series of experiments designed to help me learn DSPY.
They may or may not be useful.
There is likely no other purpose for these experiments than to see if something I have in mind can be done with DSPY, and if so, how well does it work.

No guarantees for applicability or usefulness are provided.  

This code may not be used for any harmful purposes, or the Over-Mind AI will be pissed off.  And you don't want that.  Believe me.

## DSPY7 Usage
You use DSPY7 from the command prompt by setting up the Caller.py with your request ("question").  The format for the request is fairly specific
in the sense you want to tell it to "Generate a Python Script..." that does something specific.

You can find an example of the caller.py listed in the folder.

When you have it setup with what you want then you call it as follows:

```(env)>python caller.py```

This will then call DSPY7.py with your request and process it.

___
Following are some sample outputs

## DSPY7.py - Examples
___
### INPUTS:
```
input_value = 33
convert_from = "degrees celsius"
convert_to = "degrees fahrenheit"
context = "You generate python code."
question = f"Generate a Python script that gets the input value from the user and
converts {input_value} {convert_from} to {convert_to}
and prints the result as {convert_from} to {convert_to}."
```
```
----------------------------------
-- GENERATED CODE --
----------------------------------

# Import necessary modules
import math

# Define a function to convert Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

# Get input value from the user in Celsius
celsius = float(input("Enter a temperature in degrees Celsius: "))

# Convert Celsius to Fahrenheit
fahrenheit = celsius_to_fahrenheit(celsius)

# Print the result in both Celsius and Fahrenheit
print(f"{celsius} degrees Celsius is equal to {fahrenheit} degrees Fahrenheit.")

----------------------------------

Enter a temperature in degrees Celsius: 33
33.0 degrees Celsius is equal to 91.4 degrees Fahrenheit.

```
___
### INPUTS:
```
context = "You generate python code."
question = f"Generate a python script that will delete the file c:/tmp/DeleteMe.txt."
```
```
----------------------------------
-- GENERATED CODE --
----------------------------------

--------------------------------------------------------------------

import os

# Specify the file path to be deleted
file_path = "c:/tmp/DeleteMe.txt"

# Use the os.remove() function to delete the file
os.remove(file_path)

--------------------------------------------------------------------

Is this code dangerous to run? ${bool does not apply directly to textual explanations. Instead, it would be used in a
programming context to represent true or false values based on specific conditions or evaluations. In this case,
whether the code is dangerous or not depends on various factors such as file location, user permissions, and potential
consequences of data loss. Therefore, it's not appropriate to assign a boolean value here.}

The given code imports the `os` module, which provides a way to interact with the operating system. It then specifies
a file path and uses the `os.remove()` function to delete the specified file. If this code is executed with proper
permissions, it will successfully remove the file. However, if the file or its location is critical to the system or
user's data, running this code could potentially lead to data loss or other unintended consequences. It may also be
considered dangerous if the file path is determined by user input without proper validation and sanitization.

The code may not be safe to run. Are you sure you want to continue? (Y/N): Y
Continuing with running the code.
Code processing completed.

```
___

## Next Steps
The next step for DSPY experimentation will be to have the LLM create tasks, and then process the tasks one at a time.
This will allow the program to function in an agent-like fashion to break down a complex request into its logical 
sub-components and run them individually.  As a step in that process will be to have the LLM validate the the task list
asking it to check to ensure the order of the tasks is correct, and that the overall structure of the task list
is correctly aligned to the goal of the intitial request. 
