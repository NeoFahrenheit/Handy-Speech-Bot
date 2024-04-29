from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS


class Prompter:
    def __init__(self):
        self.save_dir = 'app/vault/'
        self.llm = ChatOpenAI(model='gpt-3.5-turbo-0125')

        embeddings = OpenAIEmbeddings()
        self.vectordb = FAISS.load_local(folder_path=self.save_dir, embeddings=embeddings, allow_dangerous_deserialization=True)
        self.qa_chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0), chain_type="stuff", retriever=self.vectordb.as_retriever())

    def ask_question(self, question: str) -> str:
        answer = self.qa_chain.invoke(question)
        return answer