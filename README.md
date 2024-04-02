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

## Current Status (4/2/2024)
DSPY12.py is called by Caller12.py.  

It is run as follows:

```(env) >python caller12.py ```

It produces the following output:

```
--- START PROGRAM ---


Context: You generate top quality python code, paying careful attention to the details of the requirements.
Question: Generate Python code that converts 44 miles to feet. Then the code should convert the 44 to yards.
Then the code should print the conversion statement:  miles to feet.
Then the code should print the conversion statement:  miles to yards.
Then the code should create a file c:/temp/conversion.txt with the printed conversion statements in it.
Then the code should have error handling routines.
Then the code should print a success message, and show the name of the file and what folder the file was saved to.
------------------
Generate Tasks...
Inside GenerateTasks...
=================================================
Tasks to be processed:
1. Define a function to convert miles to feet.
2. Define a function to convert miles to yards.
3. Create a main function that uses these conversion functions.
4. Implement error handling for input validation.
5. Print the conversion statements "miles to feet" and "miles to yards".
6. Write the conversion statements into a file named "conversion.txt" at path c:/temp/.
7. Print a success message, including the name of the file and the folder it was saved to.
=================================================
Enter GenCode (0)...
Inside MultiHop 1
-- GENERATED CODE -----------------------
***python
import os

MILES_TO_FEET = 5280
MILES_TO_YARDS = 1760

try:
    miles = 44
    feet = miles * MILES_TO_FEET
    print(f"{miles} miles is equal to {feet} feet.")

    yards = miles * MILES_TO_YARDS
    print(f"{miles} miles is equal to {yards} yards.")

    with open('c:/temp/conversion.txt', 'w') as f:
        f.write(f"Miles to Feet: {feet}\n")
        f.write(f"Miles to Yards: {yards}\n")

    print("Conversion statements saved successfully in c:/temp/conversion.txt.")
except Exception as e:
    print(f"An error occurred: {e}")
***
Inside MultiHop 1
IsCodeValid: True.
isCodeValid is True...
***python
import os

MILES_TO_FEET = 5280
MILES_TO_YARDS = 1760

try:
    miles = 44
    feet = miles * MILES_TO_FEET
    print(f"{miles} miles is equal to {feet} feet.")

    yards = miles * MILES_TO_YARDS
    print(f"{miles} miles is equal to {yards} yards.")

    with open('c:/temp/conversion.txt', 'w') as f:
        f.write(f"Miles to Feet: {feet}\n")
        f.write(f"Miles to Yards: {yards}\n")

    print("Conversion statements saved successfully in c:/temp/conversion.txt.")
except Exception as e:
    print(f"An error occurred: {e}")
 
 
Validate code...
Inside ValidateCodeMatchesTask...
A *************************************
The requirements are: ['1. Define a function to convert miles to feet.',
'2. Define a function to convert miles to yards.',
'3. Create a main function that uses these conversion functions.',
'4. Implement error handling for input validation.',
'5. Print the conversion statements "miles to feet" and "miles to yards".',
'6. Write the conversion statements into a file named "conversion.txt" at path c:/temp/.',
'7. Print a success message, including the name of the file and the folder it was saved to.']
And the code is this:
import os

MILES_TO_FEET = 5280
MILES_TO_YARDS = 1760

try:
    miles = 44
    feet = miles * MILES_TO_FEET
    print(f"{miles} miles is equal to {feet} feet.")

    yards = miles * MILES_TO_YARDS
    print(f"{miles} miles is equal to {yards} yards.")

    with open('c:/temp/conversion.txt', 'w') as f:
        f.write(f"Miles to Feet: {feet}\n")
        f.write(f"Miles to Yards: {yards}\n")

    print("Conversion statements saved successfully in c:/temp/conversion.txt.")
except Exception as e:
    print(f"An error occurred: {e}")
Is it true that the code fullfil the requirements? True or False
Inside MultiHop 1
B *************************************
Prediction(
    rationale='determine if the provided code fulfills the given requirements. We will check each requirement
and see if the code matches it.\n\n1. Define a function to convert miles to feet: The code does not have a
separate function for this conversion, but it performs the conversion directly. So, it partially meets this
requirement.\n2. Define a function to convert miles to yards: Again, the code does not have a separate function
for this conversion; it performs the conversion directly. So, it partially meets this requirement as well.\n3.
Create a main function that uses these conversion functions: The provided code is already working as a main
function using the conversions. It fulfills this requirement.\n4. Implement error handling for input validation:
The code does not have any user input, so there\'s no need for input validation. However, it includes basic
exception handling with "try-except" block, which can be considered as a form of error handling. So, it partially
meets this requirement.\n5. Print the conversion statements "miles to feet" and "miles to yards": The code prints
these conversion statements as required. It fulfills this requirement.\n6. Write the conversion statements into a
file named "conversion.txt" at path c:/temp/: The provided code does exactly this using the \'open\' function and
writing the conversion values to the specified file. It fulfills this requirement.\n7. Print a success message,
including the name of the file and the folder it was saved to: The code prints a success message stating that the
conversion statements were saved successfully in the specified file and folder. It fulfills this requirement.\n\n
In conclusion, the provided code does not fully meet all requirements but comes close to fulfilling them. However,
since there are no separate functions for miles to feet and miles to yards conversions, it could be considered that
it doesn\'t strictly adhere to the exact requirements. Therefore, our answer is False. The code needs modifications
to precisely follow the given list of requirements.',
    answer='False.'
)
C *************************************
========== CodeValidated ================
Prediction(
    rationale='determine if the provided code fulfills the given requirements. We will check each requirement and see
if the code matches it.\n\n1. Define a function to convert miles to feet: The code does not have a separate function
for this conversion, but it performs the conversion directly. So, it partially meets this requirement.\n2. Define a
function to convert miles to yards: Again, the code does not have a separate function for this conversion; it performs
the conversion directly. So, it partially meets this requirement as well.\n3. Create a main function that uses these
conversion functions: The provided code is already working as a main function using the conversions. It fulfills this
requirement.\n4. Implement error handling for input validation: The code does not have any user input, so there\'s no
need for input validation. However, it includes basic exception handling with "try-except" block, which can be
considered as a form of error handling. So, it partially meets this requirement.\n5. Print the conversion statements
"miles to feet" and "miles to yards": The code prints these conversion statements as required. It fulfills this
requirement.\n6. Write the conversion statements into a file named "conversion.txt" at path c:/temp/: The provided
code does exactly this using the \'open\' function and writing the conversion values to the specified file. It
fulfills this requirement.\n7. Print a success message, including the name of the file and the folder it was saved to:
The code prints a success message stating that the conversion statements were saved successfully in the specified file
and folder. It fulfills this requirement.\n\nIn conclusion, the provided code does not fully meet all requirements but
comes close to fulfilling them. However, since there are no separate functions for miles to feet and miles to yards
conversions, it could be considered that it doesn\'t strictly adhere to the exact requirements. Therefore, our answer
is False. The code needs modifications to precisely follow the given list of requirements.',
    answer='False.'
)
=========================================
-- RUN THE FOLLOWING CODE --

--------------------------------------------------------------------

import os

MILES_TO_FEET = 5280
MILES_TO_YARDS = 1760

try:
    miles = 44
    feet = miles * MILES_TO_FEET
    print(f"{miles} miles is equal to {feet} feet.")

    yards = miles * MILES_TO_YARDS
    print(f"{miles} miles is equal to {yards} yards.")

    with open('c:/temp/conversion.txt', 'w') as f:
        f.write(f"Miles to Feet: {feet}\n")
        f.write(f"Miles to Yards: {yards}\n")

    print("Conversion statements saved successfully in c:/temp/conversion.txt.")
except Exception as e:
    print(f"An error occurred: {e}")

--------------------------------------------------------------------

os is already installed.
Required Modules are Installed
Is this code dangerous to run? False

Validate the compiled code with ast...
True
This code is safe to run and passed ast validation... compiling code...
Code is compiled... Run Code...
<code object <module> at 0x000001D1DCEDCE80, file "file", line 1>
44 miles is equal to 232320 feet.
44 miles is equal to 77440 yards.
Conversion statements saved successfully in c:/temp/conversion.txt.

Code processing completed.
Code has been processed!
```

### On Teleprompter
Along the way I tried to use Teleprompter but that turned out to be far more complicated than I felt was worth the effort.  I also noted that it made the code much more complicated, and failed to produce better results than what I could get without it.  Which is interesting.  I do want to take another look at Teleprompter in the future, but I think at this point the idea is good, but the implementation feels too complicated and I have also noted other demos on youtube where the results also turned out to be less accurate than without it.  It may be that it is useful when you fully understand all of the configuraiton options and methodologies related to its use, but in my experience it did more harm than good in this case.  So I will keep an eye on it, and try again later on when either I have a better understanding of how to configure it properly, or there is better documentation, and/or it is more matured as a feature of DSPy.

## Conclusions
I found through my experiments between DSPY7 and DSPY12 that simpler is better.  Along the way I tried breaking down each task into a separate GenCode and validation, but this turned out to not only be overly time consuming, and more complicated, but the results were far worse than the simplified version that DSPY12 turned out to be.  This is likely because breaking it down into individual code generation pieces based on each task generating code separately caused the LLM to not see the overall context of the code and therefore come up with solutions that when combined, actually didn't work well.  DSPY12 is the best of the efforts.

DSPY12 includes 
1) a simple GenCode method. 
2) a code validation that attempts to ensure the generated code actually matches the tasks derived from the original request.
3) an ast validation to ensure the code will compile.
4) a Danger Check to validate that the code is not potentially harmful to run, and if it is found dangerous then a Y/N option for the user to stop processing or continue.
5) a validation that needed components are installed, and provides a method for installing them if they are not installed.
6) a detailed print of the progress for review.

This has been utterly fascinating, and I am very grateful to the Stamford researchers for creating DSPY!  Wonderful stuff!  MultiHop and its predicotr features are really interesting and helpful. 
