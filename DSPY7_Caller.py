import subprocess

input_value = 22.2
convert_from = "degrees celsius"
convert_to = "degrees Fahrenheit"
context = "You generate python code."
question = f"Generate a Python script that converts {input_value} {convert_from} to {convert_to} and prints the result as {convert_from} to {convert_to}."

# question = "Generate a python script that will delete the file c:/temp/TestDeleteMe.txt"
# question = "Generate a python script that opens a file c:/Users/mabramsR/Desktop/PythonEnvironments/DSPY/DSPY2.py and opens a connection to a sql server 19 database named AI_Exchange on the localhost using a trusted connection."

# question = input("Please state your request: ")

subprocess.call(["python", "DSPY7.py", context, question])

