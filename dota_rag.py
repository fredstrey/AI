from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

#Load the pre-generated JSON containing Dota 2 hero lore
def load_heroes_lore(json_file):
    with open(json_file, 'r') as f:
        heroes = json.load(f)
    return heroes

#Create embeddings for each hero's lore
def create_embeddings(heroes):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = {hero: model.encode(lore) for hero, lore in heroes.items()}
    return embeddings

#Use FAISS to index the embeddings
def create_faiss_index(embeddings):
    embedding_list = list(embeddings.values())
    index = faiss.IndexFlatL2(embedding_list[0].shape[0])
    index.add(np.array(embedding_list))
    return index

# Function to retrieve relevant hero lore
def retrieve_relevant_lore(query, model, index, heroes):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=1)  # Find the most relevant hero lore
    
    if len(I[0]) > 0:
        relevant_hero = list(heroes)[I[0][0]]  # Hero name
        relevant_lore = heroes[relevant_hero]  # Hero lore (directly the value in heroes)
    else:
        relevant_hero = "Sorry, I couldn't find a relevant answer to your question."
        relevant_lore = ""
    return relevant_hero, relevant_lore


# Function for RAG - Retrieve and generate response
def skynet():
    #Load the pre-generated JSON containing the heroes' lore
    heroes = load_heroes_lore(r'C:\Users\f\Desktop\rag\herois_lore.json')
    
    #Create embeddings for each hero's lore
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = create_embeddings(heroes)
    
    #Create FAISS index for retrieval
    index = create_faiss_index(embeddings)
    
    # Initialize the language model
    ollama_model = OllamaLLM(model="llama3.2")
    
    # Template for prompt interaction with the model
    template = '''You are Skynet, an expert on Dota 2 lore, and you know the backstories of all the heroes in Dota 2.
Your job is to answer questions from users based on the lore of the heroes. You will retrieve the most relevant lore based on the user’s question.

Here is the history of conversations with Skynet (if any): {context}

Please refer to the lore of the relevant hero and, based on the lore, respond to the following question in a clear and accurate manner. If you cannot find the information, kindly let the user know that you don't have an answer.

Question: {question}
Answer:
'''
    
    # Initialize the prompt and the model chain
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | ollama_model
    
    context = ""
    
    while True:
        question = input("Enter your question: ")
        if question.lower() == "exit":
            break
        
        # Retrieve the most relevant hero lore based on the question
        relevant_hero, relevant_lore = retrieve_relevant_lore(question, model, index, heroes)
        
        # Pass the context (including the relevant hero lore) and the question to the model to generate the answer
        full_context = context + "\n" + f"Relevant Hero: {relevant_hero}\nLore: {relevant_lore}\nQuestion: {question}"
        result = chain.invoke({"context": full_context, "question": question})
        
        # Display the model's answer in English
        print("Skynet: ", result)
        
        # Update the context with the question and the generated answer
        context += f"\nUser: {question}\nSkynet: {result}"

if __name__ == "__main__":
    # Start the assistant
    skynet()
