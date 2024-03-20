import sys
import dspy
import pygments  # Assuming you have pygments installed

class Task:
  def __init__(self, description, function):
    self.description = description
    self.function = function


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
    print("-- RUN THE FOLLOWING CODE -- \n")
    code = code.replace('Â ', '')
    code = code.replace('```', '***', 1)
    code = code.replace('```', '***', 1)
    print(("--------------------------------------------------------------------\n"))
    print(code + "\n")
    print(("--------------------------------------------------------------------\n"))

    compiled_code = compile(code, 'file', 'exec')
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
      user_input = input("The code may not be safe to run. Are you sure you want to continue? (Y/N): ")

      if user_input.upper() == "Y":
        print("Continuing with running the code.\n")
        exec(compiled_code)
        print("\n" + "Code processing completed.")
      else:
        print("Exiting without running the code.")
  except SyntaxError as e:
    print(f"Error executing code: {e}")

def identify_task_type(task_description):
  keywords = {
      "code_generation": ["generate code", "write a Python function", "create a script"],
      "data_manipulation": ["filter data", "sort data", "calculate statistics"],
      "file_operation": ["read a file", "write to a file", "download a file"]
  }
  for task_type, phrases in keywords.items():
    for phrase in phrases:
      if phrase in task_description.lower():
        return task_type
  return "other"  # Default category for unidentified tasks

colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')

MyLM = dspy.OpenAI(api_base="http://localhost:1234/v1/", api_key="sk-111111",
                  model="macadeliccc/laser-dolphin-mixtral-2x7b-dpo", temperature=.40, max_tokens=7000)

dspy.settings.configure(lm=MyLM, rm=colbertv2_wiki17_abstracts)

multihop = MultiHop(MyLM)

response = multihop.forward(context=context, question=question)

# LLM output processing modified to generate tasks
generated_tasks = []
try:
  response = multihop.forward(context=context, question=question)
  tasks_data = response.answer

collected_code = []

for task in tasks_data:
  description = task["description"]
  task_type = identify_task_type(task["description"])
  
  if "code_generation" in task_type:
    # Handle code generation tasks (assuming code is already parsed and compiled)
    collected_code.append(task["code"])
  elif task_type == "data_manipulation" or task_type == "file_operation":
    max_retries = 3
    retries = 0
    while retries < max_retries:
      new_response = multihop.forward(context=context, question=task["description"])
      # Check if parsed code is available and valid Python code
      if "code" in new_response and is_valid_python_code(new_response.code):
        collected_code.append(new_response.code)
        break  # Code found, exit the retry loop
      else:
        retries += 1
        if retries < max_retries:
          print(f"Retrying code generation (attempt {retries+1} of {max_retries})")
        else:
          collected_code.append("Task could not be written as Python code.")
  else:
    # Handle other or unidentified tasks (potentially add a placeholder message)
    collected_code.append("Task description: " + description + " (Unidentified task type)")

# Display formatted code blocks
for code_block in collected_code:
  print(pygments.highlight(code_block, PythonLexer(), TerminalFormatter()))

# Prompt for confirmation
user_response = input("Do you want to execute the generated code? (Y/N): ")

if user_response.lower() == "y":
  for code_block in collected_code:
    run_python_code(code_block)
else:
  print("Code execution skipped.")
