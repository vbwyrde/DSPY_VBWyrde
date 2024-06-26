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
Earlier I thought that teleprompter (aka Optimization) was less important than it probably is, as it seems to provide the most significant advantage that DSPy offers over other LLM Programming methodologies.  I will need to look into this in more detail.  It is not necessarily simple to do, and requires a good deal of fiddling around to get setup up with it on a pipeline by pipeline basis.  You need to create (or have available) training data for your metrics, and then get things working on a try-and-see basis until you get the Optimization to be optimal for your pipeline.  I think.  At least at this point, after some more poking around at it, that seems to be the case. However, once you have your training sets for your optimizations, then DSPy should provide an optimized series of prompts for pipeline against any given model.  The caveat is that, according to some demos I've seen online, Optimization doesn't always produce better results than non-optimized DSPy programs.  So careful attention has to be paid to the results to ensure that the Optimization is actually an improvement, from what I've been seeing.  Caveat:  that condition may have already been superceded by later DSPy development, or the demos were done by people who didn't quite understand the nuances of Optimization, or they were rushing to get the demo finished, and didn't quite have the optimization configured properly for their pipelines.  Any, some, or all of those could be true.  Or, it could be that Optimization is tricky, and doesn't always provide better results.  At this point, I'm not sure.  However, it does bear looking into further.

### The Model Matters
The current version of DPSY12.py is pretty solid.  It does a lot of what one would probably want for a Python code generator.  However, depsite the effort to have it validate the code by comparing the task list it generates with the code it generates, it still is the case that lower-level models can hallucinate, and therefore produce erroneous results.  And for higher level models (such as GPT4) it is plausible that the validations being done by DSPY12.py are not necessary. Therefore, it is plausible as well that DSPY12.py is best used with upper-mid-range models (in the 33B range) that are also known to be good at coding.
For my experimentation I am using fireworks.ai because I do not have a GPU that I can use at work.  It's good, but the available models are limited at the moment.  I was trying model="accounts/fireworks/models/mistral-7b-instruct-4k", and this gave me fair, but not great results as the model tended to hallucinate its python code to some degree.  I then switched to model="accounts/fireworks/models/mixtral-8x22b-instruct", which gave me substantially better results, but still, not quite perfect.  But what with LLMs is perfect?  Since they are stochastic by nature, you cannot expect perfect.  However, it should be noted that which model you pick for which type of operation makes a gigantic difference in terms of reliability of output.  In this case we are trying to generate python code, and then have the model validate that code meets the expectations of the tasks list generated by the LLM based on the user's original request.  If the model is prone to hallucinate python code, then even with the validation, it is likely to fail to work properly since even asking it to check the code is subject to further hallucinatory results.  As a consequence:  Model Matters.  A lot.   

## Conclusions
I found through my experiments between DSPY7 and DSPY12 that simpler is better.  Along the way I tried breaking down each task into a separate GenCode and validation, but this turned out to not only be overly time consuming, and more complicated, but the results were far worse than the simplified version that DSPY12 turned out to be.  This is likely because breaking it down into individual code generation pieces based on each task generating code separately caused the LLM to not see the overall context of the code and therefore come up with solutions that when combined, actually didn't work well.  DSPY12 is the best of the efforts.

DSPY12 includes 
1) a simple GenCode method. 
2) a code validation that attempts to ensure the generated code actually matches the tasks derived from the original request.
3) an ast validation to ensure the code will compile.
4) a Danger Check to validate that the code is not potentially harmful to run, and if it is found dangerous then a Y/N option for the user to stop processing or continue.
5) a validation that needed components are installed, and provides a method for installing them if they are not installed.
6) a detailed print of the progress for review (mostly for debugging purposes to see where the interactions have weaknesses).

This has been utterly fascinating, and I am very grateful to the Stamford researchers for creating DSPY!  Wonderful stuff!  MultiHop and its predicotr features are really interesting and helpful. 
