gpt_response=[]
for i in range(len(df)):
  response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0613:devrev-inter-iit-tech-meet::8UG8JMbv",
    messages=[
      {"role": "user", "content": df.iloc[i]['query']}
    ]
  )
  gpt_response.append(response.choices[0].message.content)
  print(response.choices[0].message.content)


def infer_gpt(rag, data):
    inp_data = ""+ rag + "\n" + "Query : " + data + "\n" + "Given set of tools ,Solve the above query and return the output in JSON Format"
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0613:devrev-inter-iit-tech-meet::8UG8JMbv",
        response_format={"type": "json_object"},
        messages=[
        {"role": "user", "content": inp_data}
        ]
    )
