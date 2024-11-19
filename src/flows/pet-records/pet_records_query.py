from promptflow import tool
from promptflow.connections import CustomConnection
from azure.cosmos import CosmosClient

@tool
def get_pet(petId: str, conn: CustomConnection) -> str:
    client = CosmosClient(url= conn.endpoint, credential=conn.key)
    db = client.get_database_client(conn.databaseId)
    container = db.get_container_client(conn.containerId)
    query = f'SELECT * FROM c WHERE c.PetId = "{petId}"'

    result = container.query_items(query=query, enable_cross_partition_query=False)

    results_lists = list(result)

    return results_lists
    