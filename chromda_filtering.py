import chromadb
from chromadb.utils import embedding_functions


#Creating embedding function to generate vector embeddings
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

#creating collections
client= chromadb.Client()
collection=client.create_collection( 
    name="filter_demo",
    metadata={"description": "Used to demo filtering in ChromaDB"},
    configuration={
        "embedding_function": ef
    })

print(f"Collection created: {collection.name}")

collection.add(
    documents=[
        "This is a document about LangChain",
        "This is a reading about LlamaIndex",
        "This is a book about Python",
        "This is a document about pandas",
        "This is another document about LangChain"
    ],
    metadatas=[
        {"source": "langchain.com", "version": 0.1},
        {"source": "llamaindex.ai", "version": 0.2},
        {"source": "python.org", "version": 0.3},
        {"source": "pandas.pydata.org", "version": 0.4},
        {"source": "langchain.com", "version": 0.5},
    ],
    ids=["id1", "id2", "id3", "id4", "id5"]
)

#find all documents where the source is "langchain.com"
print(collection.get(
    where={ "source":{"$eq":"langchain.com"}  }
))
print("" \
"" \
"" \
"" \
"")
#LangChain documents with versions less than 0.3
print(collection.get(
    
    where= {"$and":[
        { "source":{"$eq":"langchain.com"}},
        {"version": {"$lt":0.3}}
    ]
    }           
          
))
print("" \
"" \
"" \
"" \
"")

#Retrieve all documents about LangChain and LlamaIndex with a version less than 0.3
print(collection.get(
    where={
        "$and":[
            {"source":{"$in":["langchain.com", "llamaindex.ai"]}},
            {"version":{"$lt":0.3}}
        ]
    }
))

# find documents that include the word "pandas" in the text
collection.get(
    where_document={"$contains":"pandas"}
)

#all documents containing "LangChain" or "Python" with version numbers greater than 0.1:
collection.get(
    where={"version": {"$gt": 0.1}},
    where_document={
        "$or": [
            {"$contains": "LangChain"},
            {"$contains": "Python"}
        ]
    }
)