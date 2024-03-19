import sys
import dspy
import re
import importlib

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python DSPY7.py <context> <question>")
        sys.exit(1)

    context = sys.argv[1]
    question = sys.argv[2]

    # Now you can use the context and question variables in your script
    print("Context:", context)
    print("Question:", question)

class MultiHop(dspy.Module):
    def __init__(self, lm, passages_per_hop=3):
        self.Generate_query = dspy.ChainOfThought("context, question -> query")
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, context, question):
        context_list = [context]  # Convert context to a list
        for _ in range(2):
            query = self.Generate_query(context=context_list[-1], question=question).query
            retrieved_passages = self.retrieve(query).passages
            context_list.extend(retrieved_passages)
        return self.generate_answer(context=context_list, question=question)


def run_python_code(code):
    try:
        print(("--------------------------------------------------------------------\n"))
        print("-- THIS IS THE GENERATED CODE -- \n")
        code = code.replace('Â ', '')
        code = code.replace('```', '***', 1)
        code = code.replace('```', '***', 1)
        print(("--------------------------------------------------------------------\n"))
        print(code + "\n")
        print(("--------------------------------------------------------------------\n"))

        InstallModule = DoesImportModuleExist(code)
        if InstallModule:
            print("Required Modules are Installed")
        else:
            print("Module was Not Installed, but is required for this script.")
            return

        compiled_code = compile(code, 'file', 'exec')
        # print("code compiled successfully")

        # HERE WE SHOULD CHECK TO SEE IF THE CODE IS DANGEROUS TO RUN
        question = "Is this code dangerous to run? " + code

        Pred = dspy.Predict("question -> rationale, bool")
        response = Pred(question=question)

        print("Is this code dangerous to run? " + str(response.bool) + "\n")

        print(response.rationale + "\n")

        if str(response.bool) == "False":
            print("This code is safe to run.  You may process the code.\n")
            exec(compiled_code)
        else:
            user_input = input("The code may not be safe to run. Are you sure you want to continue? (Y/N): ")

            if user_input.upper() == "Y":
                print("Continuing with running the code.\n")
                exec(compiled_code)
                print("\n" + "Code processing completed.")
            else:
                print("Exiting without running the code.")
    except SyntaxError as e:
        error = str(e)  # Convert the exception to a string
        return error  # Return the error string



def DoesImportModuleExist(code):
    modules = re.findall(r'import\s+(\w+)', code)
    missing_modules = []

    for module_name in modules:
        try:
            importlib.import_module(module_name)
            print(f"{module_name} is already installed.")
        except ModuleNotFoundError:
            missing_modules.append(module_name)

    if missing_modules:
        user_input = input(
            f"The following modules are not installed: {', '.join(missing_modules)}. Do you want to install them? (Y/N): ")
        if user_input.upper() == 'Y':
            import subprocess
            for module_name in missing_modules:
                subprocess.run(['pip', 'install', module_name])
            return True
        else:
            return False
    else:
        return True


def GenCode(context, question):
    multihop = MultiHop(MyLM)
    response = multihop.forward(context=context, question=question)

    try:
        generated_code = response.answer
        generated_code = generated_code.replace('Â ', '')
        generated_code = generated_code.replace('```', '***', 1)
        generated_code = generated_code.replace('```', '***', 1)

        if generated_code:
            start_marker = "***python"
            end_marker = "***"

            start = generated_code.find(start_marker) + len(start_marker)
            end = generated_code.find(end_marker, start)

            python_code = generated_code[start:end].strip()
            return python_code
    except Exception as e:
        print(str(e))
        sys.exit(1)
def RunProcess(context, question):

    retry_count = 0
    generated_python_code = GenCode(context, question)

    while retry_count < 3:
        results = run_python_code(generated_python_code)

        if isinstance(results, str):  # Check if results contain an error message
            print(f"Error occurred: {results}")
            retry_count += 1
            question_with_error = f"{question} Error: {results}"
            generated_python_code = f"{generated_python_code} {question_with_error}"
        else:
            break

    if retry_count == 3:
        print("Failed to process after 3 attempts. Stopping.")
    else:
        print("Processing completed successfully.")

colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')

MyLM = dspy.OpenAI(api_base="http://localhost:1234/v1/",
                   api_key="sk-111111",
                   model="macadeliccc/laser-dolphin-mixtral-2x7b-dpo",
                   temperature=0,
                   max_tokens=7000)

dspy.settings.configure(lm=MyLM, rm=colbertv2_wiki17_abstracts)

RunProcess(context, question)

