import importlib
import re
import sys
import ast
import dspy
import traceback

colbertv2_wiki17_abstracts = dspy.ColBERTv2(
    url="http://20.102.90.50:2017/wiki17_abstracts"
)
#MyLM = dspy.OpenAI(
#    api_base="http://localhost:1234/v1/",
#    api_key="sk-111111",
#    model="macadeliccc/laser-dolphin-mixtral-2x7b-dpo",
#    temperature=0.4,
#    max_tokens=9000,
#)
MyLM = dspy.OpenAI(
    api_base="https://api.fireworks.ai/inference/v1/",
    api_key="AaM4Ha2kUZmzr7fkAMEp6iv0QrJOpsOuAfnLaqQtH88egNA4",
    model="accounts/fireworks/models/mixtral-8x7b-instruct",            
    temperature=0.6,
    max_tokens=7000
)
print("MyLM: " + str(MyLM))
dspy.settings.configure(lm=MyLM, rm=colbertv2_wiki17_abstracts)

class MultiHop(dspy.Module):
    def __init__(self, lm, passages_per_hop=3):
        self.Generate_query = dspy.ChainOfThought("context, question -> query")
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, context, question):
        print("Inside MultiHop 1")
        context_list = [context]
        for _ in range(2):
            query = self.Generate_query(
                context=context_list[-1], question=question
            ).query
            retrieved_passages = self.retrieve(query).passages
            context_list.extend(retrieved_passages)
        return self.generate_answer(context=context_list, question=question)

class GenerateTasks(dspy.Signature):
    """Generate a list of tasks in structured format."""

    context = dspy.InputField(desc="You create a high level project task list for the python programmer that includes all relevant details.")
    question = dspy.InputField()
    tasks = dspy.OutputField(desc="Enumerated Task List", type=list)

    def forward(context, question):
        print("Inside GenerateTasks...")
        pred_generate_tasks = dspy.Predict("context, question -> tasks")
        TasksList = pred_generate_tasks(context=context, question=question)
        return TasksList

def DoesImportModuleExist(code):
    modules = re.findall(r"import\s+(\w+)", code)
    from_imports = re.findall(r"from\s+(\w+)\s+import", code)
    missing_modules = []

    for module_name in modules:
        if module_name not in from_imports:
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

def validate_python_code_ast(code):
    """
    Attempts to parse the provided Python code using ast.parse()

    Args:
      code: The Python code string to validate.

    Returns:
      True if the code can be parsed without errors, False otherwise.
    """
    try:
        ast.parse(code)
        return True
    except (SyntaxError, ParserError):
        tb = traceback.format_exc()
        print(f"There was an Error: {e}\n{tb}", file=sys.stderr)
        return False

def ValidateCodeImports(CodeBlock, task):
    print("Inside ValidateCodeImports...")
    EvalQuestion = (
        "The requirements are: "
        + str(task)
        + "\n\n"
        + "And the code is this: "
        + "\n ----------------------------------------------------- \n"
        + CodeBlock
        + "\n ----------------------------------------------------- \n"
        + "Are the python imports correct and necessary to execute this code? True or False"
    )
    print("** EVAL QUESTION PYTHON IMPORTS *****")
    print(EvalQuestion)
    multihop = MultiHop(MyLM)
    response = multihop.forward(
        context="You are a Quality Assurance expert python programmer who evalutes code to determine if it meets the requirements. Return True or False.",
        question=EvalQuestion,
    )
    print("** EVAL RESPONSE PYTHON IMPORTS *****")
    print(response)
    print("** END EVALUATION PYTHON IMPORTS ****")

    return response


def ValidateCodeMatchesTask(CodeBlock, task):
    print("Inside ValidateCodeMatchesTask...")
    EvalQuestion = (
        "The requirements are: "
        + str(task)
        + "\n\n"
        + "And the code is this: \n"
        + "\n ----------------------------------------------------- \n"
        + CodeBlock
        + "\n ----------------------------------------------------- \n"
        + "Does this code fulfill the all of requirements and are all python libraries used in the code valid and useful? True or False"
    )
    print("** EVAL QUESTION ********************")
    print(EvalQuestion)
    multihop = MultiHop(MyLM)
    response = multihop.forward(
        context="You are a Quality Assurance expert python programmer who evalutes code to determine if it meets the requirements. Return True or False.",
        question=EvalQuestion,
    )
    print("** EVAL RESPONSE ********************")
    print(response)
    print("** END EVALUATION *******************")

    return response

def run_python_code(code):
    try:
        print("-- RUN THE FOLLOWING CODE -- \n")
        code = code.replace("Â ", "")
        code = code.replace("```", "***", 1)
        code = code.replace("```", "***", 1)
        print("\n ----------------------------------------------------- \n")
        print(code + "\n")
        print("\n ----------------------------------------------------- \n")
       
        compiled_code = ""

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
            print(ast_valid)
            if ast_valid:
                print(
                    "This code is safe to run and passed ast validation... compiling code..."
                )
                compiled_code = compile(code, "file", "exec")
                print("Code is compiled... Run Code...")
                print("Here is the precompiled code that will run: \n\n")
                print("------------------------------------- \n \n")                
                print(code)
                print("------------------------------------- \n \n")                

                try:
                    print(compiled_code)
                    exec(compiled_code)
                    print("\n" + "Code processing completed.")
                except SyntaxError as e:
                    tb = traceback.format_exc()
                    print(f"There was an Error: {e}\n{tb}", file=sys.stderr)
            else:
                print("Code did not pass ast validation.")
                # ================================================
                # NOTE: HERE WE CAN USE AST TO TRY TO FIX THE CODE
                # ================================================

        else:

            print(response.rationale + "\n")
            user_input = input(
                "The code may not be safe to run. Are you sure you want to continue? (Y/N): "
            )

            if user_input.upper() == "Y":
                print("Continuing with running the code.\n")
                try:
                    print("Validate the compiled code with ast...")
                    
                    ast_valid = validate_python_code_ast(code)
                    print(ast_valid)
                    if ast_valid:
                        print(
                            "This code is safe to run and passed ast validation... compiling code..."
                        )
                        compiled_code = compile(code, "file", "exec")
                        print("Code is compiled... Run Code...")
                        try:
                            print(compiled_code)
                            exec(compiled_code, globals(), locals())
                            print("\n" + "Code processing completed.")
                        except SyntaxError as e:
                            tb = traceback.format_exc()
                            print(f"There was an Error executing the code: {e}\n{tb}", file=sys.stderr)
                    else:
                        print("Code did not pass ast validation.")
                        # ================================================
                        # NOTE: HERE WE CAN USE AST TO TRY TO FIX THE CODE
                        # ================================================
                except SyntaxError as e:
                    tb = traceback.format_exc()
                    print(f"There was an Error executing the code: {e}\n{tb}", file=sys.stderr)
            else:
                print("Exiting without running the code.")
    except SyntaxError as e:
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

def GenCode(context, task, depth=0, max_depth=5):
    print("Enter GenCode (" + str(depth) + ")...")

    multihop = MultiHop(MyLM)
    response = multihop.forward(context=context, question=task)

    try:
        generated_code = response.answer
        generated_code = generated_code.replace("Â ", "")
        generated_code = generated_code.replace("```", "***", 1)
        generated_code = generated_code.replace("```", "***", 1)
        print("-- GENERATED CODE -----------------------")
        print(generated_code)
        print("-----------------------------------------")

        isCodeValid = ValidateCodeMatchesTask(generated_code, task)
        print("IsCodeValid: " + str(isCodeValid))

        if isCodeValid:
            print("IsCodeValid is True...")
            print(generated_code)

            AreImportsValid = ValidateCodeImports(generated_code, task)
            if AreImportsValid:
                print("Import Statements are valid and useful for this code.")
            else:
                if depth >= max_depth:
                    raise ValueError("Maximum recursion depth reached")
                else:
                    context = context + " Validate and fix the import statements."
                    GenCode(context, task, depth=depth + 1)

            if generated_code:
                start_marker = "***python"
                end_marker = "***"

                start = generated_code.find(start_marker) + len(start_marker)
                end = generated_code.find(end_marker, start)

                python_code = generated_code[start:end].strip()
                return python_code
        else:
            if depth >= max_depth:
                raise ValueError("Maximum recursion depth reached")
            else:
                GenCode(context, task, depth=depth + 1)

    except Exception as e:
        print(str(e))
        sys.exit(1)

class Main:
    def __init__(self, context, question):
        self.context = context
        self.question = question

    def execute(self):
        try:
            print("--- START PROGRAM ---\n\n")
            print("Context: " + context)
            print("Question: " + question)
            print("------------------")

            print("Generate Tasks...")

            tasks_data = GenerateTasks.forward(context=context, question=question)
            tasks = tasks_data.tasks.split("\n")

            if isinstance(tasks_data, dspy.primitives.prediction.Prediction):
                compiled_task_codes = []

                tasks = tasks_data.tasks.split("\n")

                print("=================================================")
                print("Tasks to be processed:")
                for task in tasks:
                    print(task)
                print("=================================================")

                code = GenCode(context=context, task=question)
                Code_Block = process_generated_code(code)

                print("Validate code...")
                CodeValidated = ValidateCodeMatchesTask(
                    CodeBlock=Code_Block, task=tasks
                )
                print("========== CodeValidated ================")
                print(CodeValidated)
                print("=========================================")

                if CodeValidated:
                    run_python_code(Code_Block)
                    print("Code has been processed!")
                else:
                    print(f"Task code failed validation for task: {task}")

                sys.exit(1)

        except Exception as e:
            print(f"Failed to generate tasks from LLM: {e}")


if __name__ == "__main__":
    context = sys.argv[1]
    question = sys.argv[2]

    main_program = Main(context, question)
    main_program.execute()
