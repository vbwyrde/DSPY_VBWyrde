import sys
import dspy


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

  for task in tasks_data:
    description = task["description"]
    if "code" in task:
      code = task["code"].replace('Â ', '')
      compiled_code = compile(code, '<string>', 'exec')
      function = lambda: exec(compiled_code)
    else:
      function = None  # Placeholder for non-code tasks
    generated_tasks.append(Task(description, function))

except Exception as e:
  print(f"Failed to generate tasks from LLM: {e}")

# Task processing loop
for task in generated_tasks:
  print(f"Executing Task: {task.description}")
  if task.function:
    results = run_python_code(task.function.__code__)  # Access underlying function code
  else:
    print("Skipping non-code task.")