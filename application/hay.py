# hay.py

from flask import Blueprint, render_template, session, request


hay = Blueprint('hay', __name__)


@hay.route('/search', methods=['GET', 'POST'])
def search():
    username = str(session["username"])
    if request.method == 'POST':
        question = request.form['search']
        answers = tutorial1_basic_qa_pipeline(question= question,username= username)

        return render_template('search.html', answers=answers)
    return render_template('search.html')

    # answers = tutorial1_basic_qa_pipeline(question)


def tutorial1_basic_qa_pipeline(question,username):
    import logging

    logging.basicConfig(
        format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
    logging.getLogger("haystack").setLevel(logging.INFO)

    from haystack.document_stores import ElasticsearchDocumentStore
    from haystack.nodes import FARMReader, BM25Retriever

    # launch_es()

    # Connect to Elasticsearch
    document_store = ElasticsearchDocumentStore(
        host="localhost", username="elastic", password="WbLoke8xGtKNRu*RPdjd", index=f"{username}")



    retriever = BM25Retriever(document_store=document_store)

    reader = FARMReader(
        model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

    from haystack.pipelines import ExtractiveQAPipeline

    pipe = ExtractiveQAPipeline(reader, retriever)

    # Voilà! Ask a question!
    prediction = pipe.run(
        query=f"{question}", params={"Retriever": {"top_k": 3}, "Reader": {"top_k": 3}}
    )

    # print(prediction["answers"][0].meta["name"])

    return prediction["answers"]


# if __name__ == "__main__":
#     tutorial1_basic_qa_pipeline()
