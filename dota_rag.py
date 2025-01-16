from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

#Carregando o json com a lore dos heróis
def load_heroes_lore(json_file):
    with open(json_file, 'r') as f:
        heroes = json.load(f)
    return heroes

#criando os embeddings
def create_embeddings(heroes):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = {hero: model.encode(lore) for hero, lore in heroes.items()}
    return embeddings

#FAISS para indexar
def create_faiss_index(embeddings):
    embedding_list = list(embeddings.values())
    index = faiss.IndexFlatL2(embedding_list[0].shape[0])
    index.add(np.array(embedding_list))
    return index

#Função pra extrair as informações relevantes da lore dos heróis
def retrieve_relevant_lore(query, model, index, heroes):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=1)
    
    if len(I[0]) > 0:
        relevant_hero = list(heroes)[I[0][0]] 
        relevant_lore = heroes[relevant_hero] 
    else:
        relevant_hero = "Sorry, I couldn't find a relevant answer to your question."
        relevant_lore = ""
    return relevant_hero, relevant_lore


# função do RAG pra gerar as respostas
def skynet():
   
    heroes = load_heroes_lore(r'C:\Users\f\Desktop\rag\herois_lore.json')
    
    #Criando os embeddings pra cada herói
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = create_embeddings(heroes)
    
    #Criando FAISS pra indexação
    index = create_faiss_index(embeddings)
    
    # indicando o modelo
    ollama_model = OllamaLLM(model="llama3.2")
    
    #Criando o prompt (mantendo o contexto da conversa)
    template = '''You are Skynet, an expert on Dota 2 lore, and you know the backstories of all the heroes in Dota 2.
Your job is to answer questions from users based on the lore of the heroes. You will retrieve the most relevant lore based on the user’s question.

Here is the history of conversations with Skynet (if any): {full_context}

Please refer to the lore of the relevant hero and, based on the lore, respond to the following question in a clear and accurate manner. If you cannot find the information, kindly let the user know that you don't have an answer.

Question: {question}
Answer:
'''
    
    # Iniciando o modelo
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | ollama_model
    
    context = ""
    
    while True:
        question = input("Enter your question: ")
        if question.lower() == "exit":
            break
        
        # Extraindo as informações relevantes da lore dos heróis com base na pergunta do usuário
        relevant_hero, relevant_lore = retrieve_relevant_lore(question, model, index, heroes)
        
        # Passando o contexto e a lore pro modelo gerar a resposta
        full_context = context + "\n" + f"Relevant Hero: {relevant_hero}\nLore: {relevant_lore}\nQuestion: {question}"
        result = chain.invoke({"context": full_context, "question": question})
        
       
        print("Skynet: ", result)
        
        # Atualizando o contexto com a pergunta e o texto gerado
        context += f"\nUser: {question}\nSkynet: {result}"

if __name__ == "__main__":
    skynet()
