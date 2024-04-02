import subprocess

input_value = 44
convert_from = "miles"
convert_to = "feet"
convert_to2 = "yards"
context = "You generate top quality python code, paying careful attention to the details of the requirements."

question = (f"Generate Python code that converts {input_value} {convert_from} to {convert_to}."
            f" Then the code should convert the {input_value} to {convert_to2}."
            f" Then the code should print the conversion statement:  {convert_from} to {convert_to}."
            f" then the code should print the conversion statement:  {convert_from} to {convert_to2}."
            f" Then the code should create a file c:/temp/conversion.txt with the printed conversion statements in it."
            f" Then the code should have error handling routines."
            f" Then the code should print a success message, and show the name of the file and what folder the file was saved to."
            )


#
# input_value = 100
# convert_from = "degrees celsius"
# convert_to = "degrees Fahrenheit"
# context = "You generate python code."
#


# question = "Generate a python script that will delete the file c:/temp/TestDeleteMe.txt"
# question = "Generate a python script that opens a file c:/Users/mabramsR/Desktop/PythonEnvironments/DSPY/DSPY2.py and opens a connection to a sql server 19 database named AI_Exchange on the localhost using a trusted connection."

#question = input("Please state your request: ")

# compile_tasks

subprocess.call(["python", "DSPY12.py", context, question])
