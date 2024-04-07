# THIS CODE DEMONSTRATES USING FIREWORKS TO RUN A LLM ON THE FIREWORKS HOST SERVER AND GET A RESPONSE.
# TO USE THIS CODE YOU WILL NEED TO SIGN IN TO FIREWORKS AND CREATE AN API KEY TO PLUG IN HERE.
# I WAS ABLE TO DO SO FOR FREE, USING MY GOOGLE ACCOUNT TO LOG INTO FIREWORKS.
# NOTICE THAT USING OPENAI.OPENAI() REQUIRES THAT THE V1 HAVE NO FORWARD SLASH, BUT WHEN USING
# DSPY.OPENAI() THEN THE V1 REQUIRES A FORWARD SLASH DUE TO A BUG(?) IN DSPY IMPLEMENTATION.
# THAT MAY GET FIXED IN DSPY, SO IF THIS STOPS WORKING THEN TRY WITHOUT THE FORWARD SLASH AS
# THE DSPY DEVELOPERS MAY UPDATE THEIR SOURCE CODE TO FIX THIS AT SOME POINT.

import sys
import dspy
import openai
 

print("Inside TestFirework1.py...")

try:
    client = openai.OpenAI(
        base_url = "https://api.fireworks.ai/inference/v1",
        api_key="FW_API_Key",
    )
    response = client.chat.completions.create(
      model="accounts/fireworks/models/mixtral-8x7b-instruct",
      messages=[{
        "role": "user",
        "content": "Generate a python script that prints Hello World.",
      }],
    )
    print("-- TEST 2 ------------------------")
    print("Test Fireworks Usage without DSPY")
    print(response.choices[0].message.content)
    print("----------------------------------")
except Exception as e:
    print("An unexpected error occurred at 2:", str(e))


try:

    MyLM3 = dspy.OpenAI(
        api_base="https://api.fireworks.ai/inference/v1/",
        api_key="FW_API_Key",
        model="accounts/fireworks/models/mixtral-8x7b-instruct"            
    )
    print("-- TEST 3 ------------------------")
    print("MyLM-3: " + str(MyLM3))                                   
 
    prompt = "Generate a python script that prints Hello World."
    # Make the request
    response = MyLM3.basic_request(prompt=prompt)
    
    # Print the response
    # print("Response: " + str(response))
    import ast
    response_str =    str(response)
    response_dict = ast.literal_eval(response_str)
    response_str =python_code = response_dict['choices'][0]['text']
    print(python_code)
    print("----------------------------------")
 
except Exception as e:
    print("An unexpected error occurred a 3:", str(e))