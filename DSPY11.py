import importlib
import re
import sys

import dspy

colbertv2_wiki17_abstracts = dspy.ColBERTv2(
    url="http://20.102.90.50:2017/wiki17_abstracts"
)
MyLM = dspy.OpenAI(
    api_base="http://localhost:1234/v1/",
    api_key="sk-111111",
    model="macadeliccc/laser-dolphin-mixtral-2x7b-dpo",
    temperature=0.0,
    max_tokens=7000,
)
dspy.settings.configure(lm=MyLM, rm=colbertv2_wiki17_abstracts)


class GenerateTasks(dspy.Signature):
    """Generate a list of tasks in structured format."""

    context = dspy.InputField(desc="You create a high level project task list.")
    question = dspy.InputField()
    tasks = dspy.OutputField(desc="Enumerated Task List", type=list)

    def forward(context, question):
        # prompt = "Context: {context}\nQuestion: {question}\nGenerate a list of tasks in bullet points that fulfill the requirements."
        pred_generate_tasks = dspy.Predict("context, question -> tasks")
        TasksList = pred_generate_tasks(context=context, question=question)

        return TasksList


class MultiHop(dspy.Module):
    def __init__(self, lm, passages_per_hop=3):
        self.Generate_query = dspy.ChainOfThought("context, question -> query")
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, context, question):
        context_list = [context]  # Convert context to a list

        # Combine all tasks into a single string before sending to Retriever
        combined_tasks = "\n".join(question.split("\n")[1:])

        query = self.Generate_query(
            context=context_list[-1],
            question=f"Given the following tasks:\n{combined_tasks}\nWhat is the Python code to accomplish them?",
        ).query
        retrieved_passages = self.retrieve(query).passages
        context_list.extend(retrieved_passages)
        return self.generate_answer(context=context_list, question=question)


class MultiHop(dspy.Module):
    def __init__(self, lm, passages_per_hop=3):
        self.Generate_query = dspy.ChainOfThought("context, question -> query")
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, context, question):
        context_list = [context]  # Convert context to a list
        for _ in range(2):
            query = self.Generate_query(
                context=context_list[-1], question=question
            ).query
            retrieved_passages = self.retrieve(query).passages
            context_list.extend(retrieved_passages)
        return self.generate_answer(context=context_list, question=question)


class MultiHopTasks(dspy.Module):
    def __init__(self, lm, passages_per_hop=3):
        self.Generate_query = dspy.ChainOfThought("context, question -> query")
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_answer = dspy.ChainOfThought("context, question -> task_list")

    def forward(self, context, question):
        context_list = [context]  # Convert context to a list
        for _ in range(2):
            query = self.Generate_query(
                context=context_list[-1], question=question
            ).query
            retrieved_passages = self.retrieve(query).passages
            context_list.extend(retrieved_passages)
        return self.generate_answer(context=context_list, question=question)


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

def ValidateCode(code, task):
    validation_question = f"The requirements are: {task}. Does the following code fulfill them? True or False\n{code}"
    IsCodeValid = MultiHop(MyLM).forward(context="...", question=validation_question)
    return IsCodeValid.answer

def ValidateCodeMatchesTask(CodeBlock, task):
    EvalQuestion = (
        "The requirements are: "
        + task
        + "\n"
        + "And the code is this: \n"
        + CodeBlock
        + "\n"
        + "Is it true that the code fullfil the requirements? True or False"
    )
    print("A *************************************")
    print(EvalQuestion)
    multihop = MultiHop(MyLM)
    response = multihop.forward(
        context="You are an expert programm who evalutes code to determine if it meets the requirements. Return True or False.",
        question=EvalQuestion,
    )
    print("B *************************************")
    print(response)
    print("C *************************************")

    return response


def run_python_code(code):
    try:
        print("-- RUN THE FOLLOWING CODE -- \n")
        code = code.replace("Â ", "")
        code = code.replace("```", "***", 1)
        code = code.replace("```", "***", 1)
        print(
            ("--------------------------------------------------------------------\n")
        )
        print(code + "\n")
        print(
            ("--------------------------------------------------------------------\n")
        )

        InstallModule = DoesImportModuleExist(code)
        if InstallModule:
            print("Required Modules are Installed")
        else:
            print("Module was Not Installed, but is required for this script.")
            return

        compiled_code = compile(code, "file", "exec")
        # print("code compiled successfully")

        # HERE WE SHOULD CHECK TO SEE IF THE CODE IS DANGEROUS TO RUN
        question = "Is this code dangerous to run? " + code

        Pred = dspy.Predict("question -> rationale, bool")
        response = Pred(question=question)

        print("Is this code dangerous to run? " + str(response.bool) + "\n")

        print(response.rationale + "\n")

        if str(response.bool) == "False":
            print("This code is safe to run. You may process the code.\n")
            exec(compiled_code)
        else:
            user_input = input(
                "The code may not be safe to run. Are you sure you want to continue? (Y/N): "
            )

            if user_input.upper() == "Y":
                print("Continuing with running the code.\n")
                exec(compiled_code)
                print("\n" + "Code processing completed.")
            else:
                print("Exiting without running the code.")
    except SyntaxError as e:
        print(f"Error executing code: {e}")


def process_generated_code(code):
    """
    Processes the generated code by cleaning and potentially performing additional checks.
    """
    # Implement code cleaning or other processing steps here
    cleaned_code = code.replace("Â ", "")
    cleaned_code = cleaned_code.replace("```", "***", 1)
    cleaned_code = cleaned_code.replace("```", "***", 1)
    return cleaned_code


def build_code_block(context, question):
    """
    Generates, processes, and compiles the code for a given task.

    Combines all tasks into a single question before sending to MultiHop.
    """
    code = GenCode(context=context, question=question)
    processed_code = process_generated_code(code)
    return processed_code


def compile_tasks_into_one_block(tasks):
    """
    Compiles a list of task code strings into a single Python code block.

    Args:
        tasks: A list of strings, where each string represents the code for a task.

    Returns:
        A single string containing the combined code block for all tasks.

    This function iterates through the provided task codes and joins them with appropriate
    separators to create a single executable block. It ensures proper separation
    between tasks to avoid syntax errors.
    """
    # Initialize an empty string to hold the compiled code
    compiled_code_block = ""

    # Iterate over each task's code
    for task_code in tasks:
        # **Prepend each task code with two newlines**
        task_code = "\n\n" + task_code

        # Append the task's code to the compiled code block
        compiled_code_block += task_code

    # Return the compiled code block
    return compiled_code_block


def GenCode(context, task, depth=0, max_depth=5):
    print("Enter GenCode at Depth: " + str(depth))

    # print("context : " + context + "\n")
    # print("task: " + task + "\n")

    combined_tasks = "\n".join(task.split("\n")[1:])
    multihop = MultiHop(MyLM)
    response = multihop.forward(context=context, question=task)
    #response = multihop.forward(
    #    context=context,
    #    question=f"Given the following tasks:\n{combined_tasks}\nWhat is the Python code to accomplish them?",
    #)
    try:
        generated_code = response.answer
        generated_code = generated_code.replace("Â ", "")
        generated_code = generated_code.replace("```", "***", 1)
        generated_code = generated_code.replace("```", "***", 1)
        print("-----------------------------------------")
        print(generated_code)
        print("-----------------------------------------")

        isCodeValid = ValidateCode(generated_code, task)
        print("IsCodeValid: " + str(isCodeValid))
        # print(type(isCodeValid))

        if isCodeValid:
            print("isCodeValid is True...")
            print(generated_code)
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

    # ... (code for generating code)


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
                print(tasks)
                print("=================================================")
                for task_index, task in enumerate(tasks[0:], start=1):
                    # cleaned_task = task.strip(".")  # Remove trailing period if present
                    cleaned_task = task.strip("1234567890.")

                    print(
                        f"Task {task_index}: {cleaned_task}"
                    )  # Print task number and description

                    Code_Block = build_code_block(
                        context=context,
                        question=f"Generate a python script that does the following: \n{cleaned_task}",
                    )

                    print("validate code...")
                    CodeValidated = ValidateCodeMatchesTask(
                        CodeBlock=Code_Block, task=task
                    )
                    print("========== CodeValidated ================")
                    print(CodeValidated)
                    print("=========================================")
                    if CodeValidated:
                        print("Code_Block: \n" + str(Code_Block))
                        compiled_task_codes.append(Code_Block)
                    else:
                        print(f"Task code failed validation for task: {task}")

                if compiled_task_codes:
                    print("compiled Tasks:")

                    combined_code_block = compile_tasks_into_one_block(
                        compiled_task_codes
                    )
                    print("Combined Code Block:")
                    print(combined_code_block)
                    run_python_code(combined_code_block)
                else:
                    print("No valid code generated from tasks.")
        except Exception as e:
            print(f"Failed to generate tasks from LLM: {e}")


if __name__ == "__main__":
    context = sys.argv[1]
    question = sys.argv[2]

    main_program = Main(context, question)
    main_program.execute()
