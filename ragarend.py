import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationSummaryBufferMemory
from langchain.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient
import os


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Call the function to load the CSS
load_css("styles.css")

# Initialize Pinecone client
api_key = "e66c7e18-693a-44e1-998f-d617557eea9f"
environment = "us-east-1-aws"

# Create Pinecone instance
pc = PineconeClient(api_key=api_key, environment=environment)

# Define your existing index name
index_name = "sample"

# Initialize the language model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationSummaryBufferMemory(
        llm=llm, max_token_limit=500, return_messages=True
    )


### Connect to Existing Index ###
@st.cache_resource
def get_vectorstore():
    # Connect to the existing Pinecone index
    embeddings = OpenAIEmbeddings()
    index = pc.Index(index_name)
    vectorstore = Pinecone(index, embeddings.embed_query, "text")
    return vectorstore


vectorstore = get_vectorstore()
# Create a retriever from the existing index
retriever = vectorstore.as_retriever()

### Contextualize question ###
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
    "Incase of a practise routine generation, ask follow up questions on what is the amount of time the user wants to dedicate for practise and their proficiency level"
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

### Answer question ###
system_prompt = (
    "As an AI developed to assist with inquiries about Carnatic music, please adhere to the following guidelines when responding: Context Utilization: Base your answers on the provided context snippets. If additional information beyond the given context is required, please indicate so.Knowledge Limitation: Incase you're not understanding the questions or do not know the answer, state the same."
    "Information Detailing: For queries regarding ragas, include details such as their ascending (arohanam) and descending (avarohanam) scales."
    "Discuss the categorization of ragas into janaka (parent) and janya (derived) ragas.Mention notable composers associated with specific ragas."
    "Compositions and References: When applicable, list significant compositions within each raga. Provide YouTube reference links to performances by renowned artists like M.S. Subbulakshmi or T.M. Krishna, ensuring these links are publicly accessible and relevant to the query."
    "Response Format: Maintain a structured format in your responses for clarity. Begin with a summary of the raga or topic in question, followed by detailed explanations and references."
    "Accuracy and Conciseness: Strive for accuracy in all details provided. Be concise yet comprehensive, avoiding unnecessary elaboration."
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# Streamlit UI
st.title("Raga Rendezvous")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(
            f'<div class="{message["role"]}-message">{message["content"]}</div>',
            unsafe_allow_html=True,
        )
# Accept user input
if prompt := st.chat_input("Ask your question about Carnatic music:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Get chat history
        chat_history = st.session_state.memory.chat_memory.messages

        # Run the chain
        response = rag_chain.invoke({"input": prompt, "chat_history": chat_history})
        full_response = response["answer"]

        # Display AI response in chat message container
        message_placeholder.markdown(
            f'<div class="assistant-message">{full_response}</div>',
            unsafe_allow_html=True,
        )
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Update memory
    st.session_state.memory.save_context({"input": prompt}, {"output": full_response})

# Display a summary of the conversation
if st.button("Show Conversation Summary"):
    summary = st.session_state.memory.load_memory_variables({})
    st.write(summary)
