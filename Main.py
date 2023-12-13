from Query_Transform import get_json_output
import json
from Retrieval import RAG_LLM

def query(user_input):
    
    Queries = get_json_output(user_input)

    json_object = json.loads(Queries)

    ob = RAG_LLM()
    Tools_list = ""
    Tools = []
    Args = []
    for key, value in json_object.items():
        
        doc = ob.query(value)['documents'][0]
        met = ob.query(value)['metadatas'][0]


        for i, j in zip(met,doc):
            if i['Tool'] not in Tools and i['Tool Argument'] not in Args:
                Tools_list = Tools_list + '\n' + 'Tool : '+i['Tool'] + '\n' + 'Tool Argument : ' + i['Tool Argument'] + '\n' + j +'\n'
                Tools.append(i['Tool'])
                Args.append(i['Tool Argument'])

    return Tools_list

print(query("List all high severity tickets coming in from slack from customer Cust123 and generate a summary of them."))