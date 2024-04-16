from transformers import BertTokenizer

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


# Absolutely, your approach makes a lot of sense! You’re considering the importance of each part of the context_list in relation to the original question, and prioritizing the 
# preservation of the most relevant parts. This is a smart way to manage the size of the context_list while minimizing the loss of important information.
#
# Here’s a high-level outline of how you might implement this:
#
# Monitor the size of the context_list: Keep track of the number of tokens in the context_list. Once it reaches 75% of the context window size, start the summarization process.
#
# Rate the importance of each part: For each item in the context_list, use a prediction model to rate its importance to the solution. This could be based on how closely it 
# relates to the original question, or any other criteria you think is relevant.
#
# Summarize low-priority parts: Start by summarizing the parts with the lowest priority. This could be done using a text summarization algorithm or model.
#
# Check the size again: After each summarization step, check the size of the context_list again. If it’s still too large, continue with the next lowest priority part.
#
# This approach ensures that the most relevant information is preserved as long as possible, while less relevant information is summarized to save space. It’s a dynamic and adaptable 
# solution that should work well in many different scenarios. Great thinking!
