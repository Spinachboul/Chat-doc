import chromadb

def get_collection(name: str):
    client = chromadb.Client()

    existing_collections = [c.name for c in client.list_collections()]
    if name not in existing_collections:
        return client.create_collection(name)
    else:
        return client.get_collection(name)
