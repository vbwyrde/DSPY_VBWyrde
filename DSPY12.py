import dspy
import re
import io
import sys
import importlib
import traceback
import ast
from ast import parse
from io import StringIO
from transformers import BertTokenizer
from pylint import lint
from pylint.reporters import text

print("Inside DSPY12.py...")

colbertv2_wiki17_abstracts = dspy.ColBERTv2(
    url="http://20.102.90.50:2017/wiki17_abstracts"
)
# MyLM = dspy.OpenAI(
#    api_base="http://localhost:1234/v1/",
#    api_key="sk-111111",
#    model="macadeliccc/laser-dolphin-mixtral-2x7b-dpo",
#    temperature=0.6,
#    max_tokens=7000,
# )

try:
    MyLM = dspy.OpenAI(
        api_base="https://api.fireworks.ai/inference/v1/",
        api_key="API_KEY",
        # model="accounts/fireworks/models/mistral-7b-instruct-4k",
        model="accounts/fireworks/models/mixtral-8x22b-instruct",
        temperature=0.2,
        max_tokens=3000,
    )
    print("MyLM is initialized.")
    dspy.settings.configure(lm=MyLM, rm=colbertv2_wiki17_abstracts, timeout=30)
    print("Settings are configured.")

except Exception as e:
    tb = traceback.format_exc()
    print(f"There was an Error: {e}\n{tb}", file=sys.stderr)


class MultiHop(dspy.Module):
    def __init__(self, lm, passages_per_hop=3):
        self.Generate_query = dspy.ChainOfThought("context, question -> query")
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, context, question):
        print("Inside MultiHop 1")
        context_list = [context]
        tokenizer = BertTokenizer.from_pretrained(
            "bert-base-uncased"
        )  # Or whatever tokenizer you're using

        # Create a Predict object for summarization
        ContextSum = dspy.Predict("context, question -> summary")

        for _ in range(3):  # Change this number to the number of hops you want
            query = self.Generate_query(
                context=context_list[-1], question=question
            ).query
            retrieved_passages = self.retrieve(query).passages

            # Check the size of the context_list
            context_string = " ".join(context_list)
            num_tokens = len(tokenizer.tokenize(context_string))
            if num_tokens > 0.75 * tokenizer.model_max_length:
                # If the context_list is too large, summarize the first item
                context_list[0] = ContextSum(
                    context=context_list[0], question=question
                ).summary

            context_list.extend(retrieved_passages)

        return self.generate_answer(context=context_list, question=question)


class GenerateTasks(dspy.Signature):
    """Generate a list of tasks in structured format."""

    context = dspy.InputField(desc="You create a high level project task list.")
    question = dspy.InputField()
    tasks = dspy.OutputField(desc="Enumerated Task List", type=list)

    def forward(context, question):
        print("Inside GenerateTasks...")

        # NOTE: PREDICT IS INFERIOR TO CHAINOFTHOUGHT
        # pred_generate_tasks = dspy.Predict("context, question -> tasks")
        # TasksList = pred_generate_tasks(context=context, question=question)

        pred_generate_tasks2 = dspy.ChainOfThought("context, question -> tasks")
        TasksList2 = pred_generate_tasks2(context=context, question=question)

        # print("tasks: " + str(TasksList))
        #
        # print("tasks2: " + str(TasksList2))

        # USE CHAIN OF THOUGHT RESULTS
        return TasksList2


def DoesImportModuleExist(code):
    modules = re.findall(r"import\s+(\w+)", code)
    missing_modules = []

    for module_name in modules:
        try:
            importlib.import_module(module_name)
            print(f"{module_name} is already installed.")
        except ModuleNotFoundError:
            missing_modules.append(module_name)

    if missing_modules:
        user_input = input(
            f"The following modules are not installed: {', '.join(missing_modules)}. Do you want to install them? (Y/N): "
        )
        if user_input.upper() == "Y":
            import subprocess

            for module_name in missing_modules:
                subprocess.run(["pip", "install", module_name])
            return True
        else:
            return False
    else:
        return True



def identify_language(code):
  """
  Attempts to identify the name of the programming language of the provided code snippet.

  Args:
      code: The code string to identify.

  Returns:
      A string representing the identified programming language name, e.g., 'python', 'csharp', 'vbnet', etc.
  """
  context = "You are a programming expert who can determine the language name that a code block is written in."
  question = code[:100]

  def forward(context, question):
    pred_Language = dspy.Predict("context, code_snip -> code_language")
    ProgLanguage = pred_Language(context=context, code_snip=question)
    print("Inside identify_language forward()")
 
    parts = ProgLanguage.code_language.split("\n")
    code_language = parts[0].strip()
    print("Language:" + code_language.lower().strip())
    
    return  code_language.lower()

  return forward(context, question)


def validate_python_code_ast(code):
    """
    Validates Python code syntax and optionally performs additional checks.

    Args:
        code: The Python code string to validate.

    Returns:
        A tuple containing:
            - is_ast_valid: Boolean indicating if the code is syntactically valid (based on ast.parse).
            - additional_checks: List of results from any additional checks performed (empty list if none).
    """
    print("Inside validate_python_code_ast...")

    is_ast_valid = True
    additional_checks = []
    error_message = ""
    
    try:
        # Validate basic syntax using ast.parse
        parse(code)
    except SyntaxError as e:
        is_ast_valid = False
        error_message = str(e)


    # Optionally perform additional checks using libraries like pylint  
    try:
        # Pylint check (example)
        print("linter validation...")
        
        # Assuming 'code' is the string of code you want to lint
        # Write the code to a temporary file
        with open('temp_file.py', 'w') as temp_file:
            temp_file.write(code)
        
        # Initialize a StringIO object to capture the output
        pylint_output = StringIO()
        
        # Run Pylint on the temporary file
        pylint.lint.Run(['temp_file.py'], reporter=text.TextReporter(pylint_output), exit=False)
        
        # Get the output
        output = pylint_output.getvalue()
        
        # Parse the output to get the number of warnings
        # This is a simplified example; parsing the output for specific information would require more sophisticated parsing
        warnings_count = output.count('warning')
        
        # Append the count of warnings to additional_checks
        additional_checks.append(f"Pylint warnings: {warnings_count}")

    except Exception as e:
        # Handle potential errors during additional checks
        print(f"Error during additional checks: {e}")
        error_message = error_message + ", " + str(e)

    return is_ast_valid, additional_checks, error_message


def ValidateCodeMatchesTask(CodeBlock, task):
    print("Inside ValidateCodeMatchesTask...")
    EvalQuestion = (
        "The requirements are: "
        + str(task)
        + "\n\n"
        + "And the code is this: \n"
        + "----------------------------------------------------- \n"
        + CodeBlock
        + "\n"
        + "----------------------------------------------------- \n"
        + "Does this code fulfill each and every requirement in the task list? True or False"
    )
    print("** EVAL QUESTION ******************************************************* \n")
    print(EvalQuestion)
    multihop = MultiHop(MyLM)
    response = multihop.forward(
        context="You are a Quality Assurance expert python programmer who evalutes code to determine if it meets all of the the requirements.  Every item in the task list must be met by the code. Return True or False.",
        question=EvalQuestion,
    )
    print("** EVAL RESPONSE ****************************************************** \n")
    print(response.rationale)
    print("** END EVALUATION ***************************************************** \n")

    return response


def run_code(Code_Block, language):
    print("Running the code...")
    if language.lower() == "python":
        try:
            print(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n"
            )
            run_python_code(Code_Block)
            print(
                "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n"
            )
        except Exception as e:
            print(f"Failed to run code: {e}")
            sys.exit(1)
    else:
        print("This is non-executable source code so we will not run it.")


def run_python_code(code):
    try:
        print("-- RUN THE FOLLOWING CODE -- \n")
        code = code.replace("Â ", "")
        code = code.replace("```", "***", 1)
        code = code.replace("```", "***", 1)
        print("--------------------------------------------------------------------\n")

        print(code + "\n")
        print("--------------------------------------------------------------------\n")

        InstallModule = DoesImportModuleExist(code)
        if InstallModule:
            print("Required Modules are Installed")
        else:
            print("Module was Not Installed, but is required for this script.")
            return

        question = "Is this code dangerous to run? " + code

        Pred = dspy.Predict("question -> rationale, bool")
        response = Pred(question=question)

        print("Is this code dangerous to run? " + str(response.bool) + "\n")

        if str(response.bool) == "False":
            print("Validate the compiled code with ast...")

            ast_valid = validate_python_code_ast(code)

            print("Is AST Validated: " + str(ast_valid))

            if ast_valid[0]:
                print(
                    "This code is safe to run and passed ast validation... compiling code..."
                )
                compiled_code = compile(code, "file", "exec")
                print("Code is compiled... Run Code...")
                try:
                    print(compiled_code)
                    exec(compiled_code)
                    print("\n" + "Code processing completed.")
                    return True
                except Exception as e:
                    tb = traceback.format_exc()
                    print(f"There was an Error: {e}\n{tb}", file=sys.stderr)
                    return e
            else:
                print("Code did not pass ast validation.")
                return "AST_FAIL"

        else:
            print(response.rationale + "\n")
            user_input = input(
                "The code may not be safe to run. Are you sure you want to continue? (Y/N): "
            )

            if user_input.upper() == "Y":
                print("Continuing with running the code.\n")
                compiled_code = compile(code, "file", "exec")
                print("Code is compiled... Run Code...")
                try:
                    print(compiled_code)
                    exec(compiled_code)
                    print("\n" + "Code processing completed.")
                except Exception as e:
                    tb = traceback.format_exc()
                    print(f"There was an Error: {e}\n{tb}", file=sys.stderr)
            else:
                print("Exiting without running the code.")
    except Exception as e:
        tb = traceback.format_exc()
        print(f"There was an Error: {e}\n{tb}", file=sys.stderr)


def process_generated_code(code):
    """
    Processes the generated code by cleaning and potentially performing additional checks.
    """
    # Implement code cleaning or other processing steps here
    cleaned_code = code.replace("Â ", "")
    cleaned_code = cleaned_code.replace("```", "***", 1)
    cleaned_code = cleaned_code.replace("```", "***", 1)
    return cleaned_code


def extract_code_block(generated_code, inpLanguage):
    print("Inside extract_code_block...")

    # SET CODE BLOCK IN CASE NO MARKERS ARE FOUND
    code_block = generated_code
    language = ""
    # Find the start of the code block
    start_marker_pattern = r"```(\w+)?"
    start_match = re.search(start_marker_pattern, generated_code)
    if start_match:
        start_marker = start_match.group()
        start_index = start_match.start()

        # Find the end of the code block
        end_marker = start_marker[:3]
        end_index = generated_code.find(end_marker, start_index + len(start_marker))
        if end_index != -1:
            code_block = generated_code[
                start_index + len(start_marker) : end_index
            ].strip()

            # Determine the language
            language_match = re.search(r"(\w+)", start_marker)
            if language_match:
                language = language_match.group(1).lower()
            else:
                language = None

            if inpLanguage != language:
                print("Note: input language did not match found language")
                print(
                    "inpLanguage: " + str(inpLanguage) + ", Language: " + str(language)
                )

            return code_block

    return code_block, language


def GenCode(context, task, depth=0, max_depth=5):
    """
    Generates code using MultiHop with a limited recursion depth.

    Args:
        context: The context string for the code generation.
        task: The task description for the code to fulfill.
        depth: Current recursion depth (internal use).
        max_depth: Maximum allowed recursion depth.

    Returns:
        The generated code if successful, None otherwise.

    Raises:
        ValueError: If the maximum recursion depth is reached.
    """
    print("Enter GenCode (" + str(depth) + ")...")

    multihop = MultiHop(MyLM)
    response = multihop.forward(context=context, question=task)

    try:
        generated_code = response.answer
        print("-- GENERATED CODE -----------------------")
        print(generated_code)
        print("-----------------------------------------")

        isCodeValid = ValidateCodeMatchesTask(generated_code, task)
        print("IsCodeValid: " + str(isCodeValid.answer))

        if isCodeValid:
            print("IsCodeValid is True...")
            print(generated_code)
            return generated_code  # The generated code can come with explanation text

        else:
            if depth >= max_depth:
                raise ValueError("Maximum recursion depth reached")
            else:
                # Retry with updated context including rationale if not max depth
                GenCode(
                    context + " rationale: " + isCodeValid.rationale,
                    task,
                    depth=depth + 1,
                )

    except Exception as e:
        tb = traceback.format_exc()
        print(f"There was an Error: {e}\n{tb}", file=sys.stderr)

        sys.exit(1)

    return None  # No valid code generated within recursion limit


class Main:
    def __init__(self, context, question):
        self.context = context
        self.question = question

    def execute(self):
        try:
            print("\n--- START PROGRAM ---\n")
            print("Inside Main.Execute()")         
            print("Context: " + self.context)
            print("Question: " + self.question)
            print("------------------")

            print("Generate Tasks...")
            tasks_data = GenerateTasks.forward(
                context=self.context, question=self.question
            )
            tasks = tasks_data.tasks.split("\n")

            if isinstance(tasks_data, dspy.primitives.prediction.Prediction):
                print("=================================================")
                print("Tasks to be processed:")
                for task in tasks:
                    print(task)
                print("=================================================")

            try:
                code = GenCode(context=self.context, task=self.question)
                language = identify_language(code).lower()

                # EXTRACT JUST THE CODE BLOCK IF POSSIBLE - IF NOT RETURN THE ORIGINAL CODE
                code = extract_code_block(code, language)

                if language == "python":
                    Code_Block = process_generated_code(code)
                else:
                    Code_Block = code[0]

                print("Code Language: " + str(language.lower()))

                print("Validating code...")
                CodeValidated = ValidateCodeMatchesTask(CodeBlock=Code_Block, task=tasks)
                print("Is code valid: " + str(CodeValidated.answer))

                if CodeValidated:
                    
                    CodeTaskValidated = True
                    ASTValidated = True
                    
                    if language.lower() == "python":
                        ast_valid = validate_python_code_ast(Code_Block)
                        
                        print("AST Validation A: " + str(ast_valid))
                        
                        if not ast_valid[0]:
                            print(f"Code failed AST validation.")
                            # Add the error message to the context
                            self.context += (
                                f"\n The python code failed AST validation. Please refactor the code to fix any errors: "
                                + Code_Block
                                + "\n Error:"
                                + ast_valid[2]  #ast_valid[2] contains the error messages from the validation procedure
                            )
                            # Recursively call GenCode with the updated context
                            code = GenCode(context=self.context, task=self.question)
                            Code_Block = process_generated_code(code)
                            # Validate the new code
                            CodeTaskValidated = ValidateCodeMatchesTask(CodeBlock=Code_Block, task=tasks)  
                            ASTValidated = validate_python_code_ast(Code_Block)
                            
                        if CodeTaskValidated and ASTValidated:
                            print("Code has been processed!")
                            with open("c:/Temp/Generated_code.txt", "w") as file:
                                file.write(Code_Block)
                            run_code(Code_Block=Code_Block, language=language)   
                            
                    else:
                        print("Code has been processed!")
                        with open("c:/Temp/Generated_code.txt", "w") as file:
                            file.write(Code_Block)
                        print(
                            "This code is non-executable "
                            + language
                            + " source code, therefore we will not attempt to run it. Code has been saved to disk instead."
                        )
                else:
                    print(f"Task code failed validation for task: {task}")
                    sys.exit(1)
            except ValueError as e:
                if "maximum recursion depth reached" in str(e):
                    print(
                        f"Error: Maximum recursion depth reached for generating code. Consider adjusting max_depth in GenCode or reformulating the task description."
                    )
                else:
                    raise e  # Raise other ValueErrors

        except Exception as e:
            tb = traceback.format_exc()
            print(f"There was an Error in Main(): {e}\n{tb}", file=sys.stderr)


if __name__ == "__main__":
    # context = sys.argv[1]
    # question = sys.argv[2]

    # context = "You generate python code."
    # question = "Generatea python script that prints 'hello world' to the console."

    # input_value = 76
    # convert_from = "miles"
    # convert_to = "feet"
    # convert_to2 = "yards"
    # context = "You generate top quality python code, paying careful attention to the details of the requirements."
    # 
    # question = (f"Generate Python code that converts {input_value} {convert_from} to {convert_to}."
    #             f" Then convert the {input_value} to {convert_to2}."
    #             f" Then print the conversion statement:  {convert_from} to {convert_to}."
    #             f" then print the conversion statement:  {convert_from} to {convert_to2}."
    #             f" Then create a file c:/temp/conversion.txt with the printed conversion statements in it."
    #             f" Then perform this calculation:  x = 1/0 "
    #             f" Then have error handling routines using traceback."
    #             f" Then print a success message, and show the name of the file and what folder the file was saved to."
    #             )
   
    context = (
        "You generate top quality, professional, vb.net code, paying careful attention to the details to ensure your code meets the requirements."
        " You always double check your code to ensure nothing has been left out."
        " Your job is to only write the code, and that is all.  Your job is only to write the vb.net code, not to create the project, deploy or to test it."
    )
    
    question = (
        f" Generate a windows service in vb.net that monitors the windows events log."
        f" The windows service should use an ai model hosted at http://localhost:1234/v1/ in order to provide an Alert when unusual behavior is occuring on the machine that indicates a high probability of the existance of a virus or hacker."
        f" The windows service should send the Alert by email to vbwyrde@yahoo.com when the service indicates the existance of a virus or hacker."
        f" The windows service should use professional error handling."
        f" The windows service should log any virus or hacker Alerts to c:/Temp/AIMonitor.log"
    )

    print("Inside Main()...")
    print(context)
    print(question)
    main_program = Main(context, question)
    main_program.execute()
