 
import re
import sys
import ast
import dspy
import importlib
import traceback
from transformers import BertTokenizer

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
        #model="accounts/fireworks/models/mistral-7b-instruct-4k",
        model="accounts/fireworks/models/mixtral-8x22b-instruct",
        temperature=0.6,
        max_tokens=3000,
    )
    print("MyLM is initialized.")
    dspy.settings.configure(lm=MyLM, rm=colbertv2_wiki17_abstracts, timeout=30)
    print("Settings are configured.")
    
except Exception as e:
    tb = traceback.format_exc()
    print(f"There was an Error: {e}\n{tb}", file=sys.stderr)


def identify_language(code):
    """
    Attempts to identify the language of the provided code snippet.

    Args:
      code: The code string to identify.

    Returns:
      A string representing the identified language, e.g., 'python', 'csharp', 'vbnet', etc.
    """
    """Determine the programming language and return the language name as a string."""

    # Define the context and question as strings directly, not as dspy.InputField objects
    contextL = "You are a programming expert who can determine what language a code block is written in."
    questionL = "What is the name of the programming language of this code: " + code

    def forward(contextL, questionL):
        print("Inside identify_language...")
        
        # NOTE: PREDICT IS INFERIOR TO CHAINOFTHOUGHT
        pred_Language1 = dspy.Predict("context, code -> language")
        ProgLanguage1 = pred_Language1(context=contextL, code=questionL) # Ensure 'code' is correctly passed
        
        #pred_Language2 = dspy.ChainOfThought("context, code -> language")
        #ProgLanguage2 = pred_Language2(context=contextL, code=questionL) # Ensure 'code' is correctly passed
        
        #print("ProgLanguage1: " + str(ProgLanguage1.language))
        #print("ProgLanguage2: " + str(ProgLanguage2.language))
        
        # USE CHAIN OF THOUGHT RESULTS
        return str(ProgLanguage1.language)

    # Call the forward function with the appropriate arguments
    return forward(contextL, questionL)

    
class MultiHop(dspy.Module):
    def __init__(self, lm, passages_per_hop=3):
        self.Generate_query = dspy.ChainOfThought("context, question -> query")
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, context, question):
        print("Inside MultiHop 1")
        context_list = [context]
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')  # Or whatever tokenizer you're using
    
        # Create a Predict object for summarization
        ContextSum = dspy.Predict("context, question -> summary")
    
        for _ in range(3):  # Change this number to the number of hops you want
            query = self.Generate_query(
                context=context_list[-1], question=question
            ).query
            retrieved_passages = self.retrieve(query).passages
    
            # Check the size of the context_list
            context_string = ' '.join(context_list)
            num_tokens = len(tokenizer.tokenize(context_string))
            if num_tokens > 0.75 * tokenizer.model_max_length:
                # If the context_list is too large, summarize the first item
                context_list[0] = ContextSum(context=context_list[0], question=question).summary
    
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
        
        #print("tasks: " + str(TasksList))
        #
        #print("tasks2: " + str(TasksList2))
        
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


def validate_python_code_ast(code):
    """
    Attempts to parse the provided Python code using ast.parse()

    Args:
      code: The Python code string to validate.

    Returns:
      True if the code can be parsed without errors, False otherwise.
    """
    try:
        print("AST Validation of code: \n", code)
        ast.parse(code)
        print("AST Validation Passed...")
        return True
    except Exception as e:
        tb = traceback.format_exc()
        print(f"There was an Error: {e}\n{tb}", file=sys.stderr)
        return e

def ValidateCodeMatchesTask(CodeBlock, task):
    print("Inside ValidateCodeMatchesTask...")
    EvalQuestion = (
        "The requirements are: "
        + str(task)
        + "\n\n"
        + "And the code is this: \n"
        + "----------------------------------------------------- \n"
        + CodeBlock + "\n"
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

#def run_code(Code_Block):
#    print("Running the code...")
#    try:
#        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
#        run_python_code(Code_Block)
#        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
#    except Exception as e:
#        print(f"Failed to run code: {e}")
#        sys.exit(1)

def run_code(Code_Block, language):
    print("Running the code...")
    if language.lower() == "python":
        try:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
            run_python_code(Code_Block)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
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
            
            if ast_valid:
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
            code_block = generated_code[start_index + len(start_marker):end_index].strip()
            
            # Determine the language
            language_match = re.search(r"(\w+)", start_marker)
            if language_match:
                language = language_match.group(1).lower()
            else:
                language = None
            
            if inpLanguage != language:
                print("Note: input language did not match found language")
                print("inpLanguage: " + str(inpLanguage) + ", Language: " + str(language))
                
            return code_block 
    
    return code_block, language

def GenCode(context, task, depth=0, max_depth=5):
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
            return generated_code   #THE GENERATED CODE CAN COME WITH EXPLANATION TEXT, SO WE WILL TRY TO EXTRACT THE CODE AFTER
            
        else:
            if depth >= max_depth:
                raise ValueError("Maximum recursion depth reached")
            else:
                # IF THE CODE DID NOT COME BACK AS VALID THEN RETRY INCLUDING THE RATIONALE GIVEN FOR THE INVALID CODE
                GenCode(context + " rationale: " + isCodeValid.rationale, task, depth=depth + 1)

    except Exception as e:
        tb = traceback.format_exc()
        print(f"There was an Error: {e}\n{tb}", file=sys.stderr)

        sys.exit(1)


class Main:
    def __init__(self, context, question):
        self.context = context
        self.question = question

    def execute(self):
       try:
           print("\n--- START PROGRAM ---\n")
           print("Context: " + context)
           print("Question: " + question)
           print("------------------")
    
           print("Generate Tasks...")
           tasks_data = GenerateTasks.forward(context=context, question=question)
           tasks = tasks_data.tasks.split("\n")
    
           if isinstance(tasks_data, dspy.primitives.prediction.Prediction):
               print("=================================================")
               print("Tasks to be processed:")
               for task in tasks:
                   print(task)
               print("=================================================")
    
               code = GenCode(context=context, task=question)
               language = identify_language(code)
               
               # EXTRACT JUST THE CODE BLOCK IF POSSIBLE - IF NOT RETURN THE ORIGINAL CODE 
               code = extract_code_block(code, language.lower())

               if language.lower() == "python":
                   Code_Block = process_generated_code(code)
               else:
                   Code_Block = code
 
               print("Language: " + str(language.lower()))
               
               print("Validating code...")
               CodeValidated = ValidateCodeMatchesTask(CodeBlock=Code_Block, task=tasks)
               print("Is code valid: " + str(CodeValidated.answer))
    
               if CodeValidated:
                   
                   if language.lower() == "python":
                       ast_valid = validate_python_code_ast(Code_Block)
                       print("AST Validation A: " + str(ast_valid))
                       if not ast_valid:
                           print(f"Code failed AST validation.")
                           # Add the error message to the context
                           self.context += f"\n Unfortunately, the following python code failed AST validation. Please regenerate the code and fix this error: " + Code_Block + "\n Error:" + ast_valid
                           # Recursively call GenCode with the updated context
                           code = GenCode(context=self.context, task=self.question)
                           Code_Block = process_generated_code(code)
                           # Validate the new code
                           CodeTaskValidated = ValidateCodeMatchesTask(CodeBlock=Code_Block, task=tasks)         # WIP - SIMPLIFY - BEING CALLED TWICE
                           ASTValidated = validate_python_code_ast(Code_Block)
                           if CodeTaskValidated and ASTValidated:
                               print("Code has been processed!")
                               run_code(Code_Block)
                           else:
                               print("Code failed validation.")
                               sys.exit(1)
                       else:
                           print("Code has been processed!")
                           run_code(Code_Block)
                   else:
                        with open("c:/Temp/Generated_code.txt", "w") as file:
                            file.write(Code_Block)
                        print("This code is non-executable "+language+" source code, therefore we will not attempt to run it.  Code has been saved to disk instead.")
               else:
                   print(f"Task code failed validation for task: {task}")
                   sys.exit(1)
       except Exception as e:
           tb = traceback.format_exc()
           print(f"There was an Error in Main(): {e}\n{tb}", file=sys.stderr)

if __name__ == "__main__":
    #context = sys.argv[1]
    #question = sys.argv[2]
    
    #context = "You generate python code."
    #question = "Generatea python script that prints 'hello world' to the console."
    
    context = ("You generate top quality, professional, vb.net code, paying careful attention to the details to ensure your code meets the requirements." 
               " You always double check your code to ensure nothing has been left out."
               " Your job is to only write the code, and that is all.  Your job is only to write the vb.net code, not to create the project, deploy or to test it."
               )
               
    question = (f" Generate a windows service in vb.net that monitors the windows events log."
                f" The windows service should use an ai model hosted at http://localhost:1234/v1/ in order to provide an Alert when unusual behavior is occuring on the machine that indicates a high probability of the existance of a virus or hacker."
                f" The windows service should send the Alert by email to somebody@yahoo.com when the service indicates the existance of a virus or hacker."
                f" The windows service should use professional error handling."
                f" The windows service should log any virus or hacker Alerts to c:/Temp/AIMonitor.log"
                )

    print("Inside DSPY12.py...")
    print(context)
    print(question)
    main_program = Main(context, question)
    main_program.execute()
