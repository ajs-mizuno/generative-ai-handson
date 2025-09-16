import os
import weaviate
from dotenv import load_dotenv

# LangChain 関連
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from langchain.chains import RetrievalQA

# 1. 接続情報の読込
load_dotenv()


def query_db(query):

    # 2. Weaviate クライアント初期化 (ローカル)
    client = weaviate.connect_to_local()

    # 3. Embeddings モデルの初期化
    embeddings = AzureOpenAIEmbeddings(
        deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_MODEL"),
        api_version=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_API_VERSION")
    )

    # 4. WeaviateVectorStore のセットアップ
    vectorstore = WeaviateVectorStore(
        client=client,
        index_name="Document",       # Weaviate 側のクラス名
        text_key="content",          # プロパティ名 (本文格納フィールド)
        embedding=embeddings,
    )

    # 5. Retriever の取得 (上位 k 件)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 6. LLM モデルの初期化
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_LLM_DEPLOYMENT_MODEL"),
        api_version=os.getenv("AZURE_OPENAI_LLM_DEPLOYMENT_API_VERSION")
    )

    # 7. RetrievalQA チェーンの構築
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",                  # "stuff" / "map_reduce" / "refine" など
        return_source_documents=False        # True にするとソースを返す
    )

    # 8. 実際にクエリを実行
    answer = qa_chain.invoke(query)

    # 9. クライアントのクローズ
    client.close()

    # 　回答を返す
    return answer["result"]
