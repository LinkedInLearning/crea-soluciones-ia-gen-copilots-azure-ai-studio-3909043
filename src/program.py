import os  
from openai import AzureOpenAI  

endpoint = os.getenv("ENDPOINT_URL", "https://ai-hub4626496556211.openai.azure.com/")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")  
search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://creasolucionesgenaisearch1.search.windows.net/")  
search_key = os.getenv("SEARCH_KEY", "Rn5i9hzT5N8RPmESikGA01qetJKZ95AKUpOsvqqY2uAzSeBio1Yd")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "8nZLVlEhyLNjizvy6eNxGkJohOmkmr1fjIY6pSzXWIj7oiSJ4tCqJQQJ99AKACfhMk5XJ3w3AAAAACOGzxwF")  

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(  
azure_endpoint=endpoint,  
api_key=subscription_key,  
api_version="2024-05-01-preview",  
)  

# Prepare the chat prompt  
chat_prompt = [
    {
        "role": "system",
        "content": "You are an AI assistant that helps people find information."
    },
    {
        "role": "user",
        "content": "Quién es Gianni?"
    }
]  

# Include speech result if speech is enabled  
speech_result = chat_prompt  

# Generate the completion  
completion = client.chat.completions.create(  
    model=deployment,  
    messages=speech_result,
    #past_messages=10,  
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,  
    stop=None,  
    stream=False  
    ,extra_body={
        "data_sources": [{
            "type": "azure_search",
            "parameters": {
            "filter": None,
            "endpoint": f"{search_endpoint}",
            "index_name": "pet-records-index",
            "semantic_configuration": "azureml-default",
            "authentication": {
                "type": "api_key",
                "key": f"{search_key}"
            },
            "embedding_dependency": {
                "type": "endpoint",
                "endpoint": "https://ai-hub4626496556211.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-07-01-preview",
                "authentication": {
                "type": "api_key",
                "key": "8nZLVlEhyLNjizvy6eNxGkJohOmkmr1fjIY6pSzXWIj7oiSJ4tCqJQQJ99AKACfhMk5XJ3w3AAAAACOGzxwF"
                }
            },
            "query_type": "vector_simple_hybrid",
            "in_scope": True,
            "role_information": "You are an AI assistant that helps people find information.",
            "strictness": 3,
            "top_n_documents": 5
            }
        }]
    })   

#print(completion.to_json())
print(completion.choices[0].message.content)