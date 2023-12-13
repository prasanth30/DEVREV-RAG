from openai import OpenAI

def get_json_output(user_query):

    api_key = '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'
    client = OpenAI(api_key=api_key)

    # Your base input
    inp = f'''
        Query:
        {user_query}

        Here's a Query. Transform the given query into distinct sentences, following the provided examples.ONLY OUTPUT AS JSON :

        Example 1.:
        Query: Prioritize my P0 issues and add them to the current sprint.

        Output:
        {{
        "sentence1": "Address my specific issue.",
        "sentence2": "Emphasize the prioritization of P0 issues.",
        "sentence3": "Add listed issues to the current sprint."
        }}

        Example 2.:
        Query: Summarize high severity tickets from the customer UltimateCustomer

        Output:
        {{
            "sentence1" : "search for customer",
            "sentence2" : "List high severity tickets Coming from 'UltimateCustomer'",
            "sentence2" : "Summarise them"
        }}
    '''

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": inp}
        ]
    )

    # Return the JSON content
    return completion.choices[0].message.content
