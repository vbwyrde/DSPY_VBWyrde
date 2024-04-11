import subprocess

# input_value = 44
# convert_from = "degrees fahrenheit"
# convert_to = "degrees celsius"
# convert_to2 = "degrees Kelvin"
# context = "You generate top quality python code, paying careful attention to the details of the requirements."
# 
# 
# question = (f"Generate Python code that converts {input_value} {convert_from} to {convert_to}."
#             f" Then the code should convert the {input_value} to {convert_to2}."
#             f" Then the code should print the conversion statement:  {convert_from} to {convert_to}."
#             f" then the code should print the conversion statement:  {convert_from} to {convert_to2}."
#             f" Then the code should create a file c:/temp/conversion.txt with the printed conversion statements in it."
#             f" Then the code should have error handling routines, and print any errors to the console."
#             f" Then the code ensure that all variables and functions are correctly created and referenced."
#             f" Then the code should print a success message, and show the name of the file and what folder the file was saved to."
#             )
# 
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

context = "You generate top quality python code, paying careful attention to the details to ensure your code meets the requirements. You always triple check your code to ensure nothing has been left out."
question = (f" Generate Python code that uses pyodbc to make a sql 2019 connection to the localhost database StylishCSS using a trusted connection."
            f" Then the code should loads the contents of C:\\inetpub\\wwwroot\\Elthos_ODS_Web\\App_Themes\\common.css into the StylishCSS.dbo.REF_CSS  row by row so that each line in the file is added as a row in the table."
            f" The code should use the following Stored Procedure to do so:"
            f" I_REF_CSS @Name As VarChar(255), @FilePathName As Text, @RowNumber As Integer, @RowContent As Text "
            f" Ensure the pyodbc code commits the transaction at the end of the loop so the data saves to the table."
            f" Ensure the code should have error handling routines, and print any errors to the console, using traceback to also include line number of the error."
            f" Then ensure that all variables and functions are correctly created and referenced."
            f" Then ensure that all python libraries and modules are valid and useful for this code."
            f" Then execute the code and print a success message showing how many rows were added to the table."
            f" Then save the code to a file named C:\\Temp\\CSS_Code.py."
            f" Then create an html page with mermaid.js flowchart TD, to diagram the function calls of the python script, and save to C:\\Temp\\CSS_Code_Flow.html."
            f" Use the following format for the HTML File, and do not use square brackets for sql objects or it will break the mermaid js file:                    "
            f"       <pre class=""mermaid"">               "
            f"        flowchart TD                         "
            f"          A[fill in here] --> B[fill in here]"
            f"       </pre>                                "
            f"       <script type=module>                  "
            f"           import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';"
            f"       </script>                             "
            f" When saving code to a file, be sure to handle the code block quotes by using single quotes for the inner block and double quotes for the outer block or the file will not save correctly."
            f" Last, ask the user if they want to use a python command to execute the code in C:\\Temp\\CSS_Code.py"
            )

subprocess.call(["python", "C:\\Users\\mabramsR\\source\\repos\\DSPY_MA\\DSPY12.py", context, question])
