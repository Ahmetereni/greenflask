
def preprocessor(filepath, filename, username, extension):
    from haystack.nodes import PreProcessor, PDFToTextConverter, DocxToTextConverter, TextConverter
    from haystack.document_stores import ElasticsearchDocumentStore

    # from haystack.utils import launch_es
    # launch_es()
    document_store = ElasticsearchDocumentStore(
        host="localhost", username="elastic", password="7-ifabNuufFkE8wxLn8f ", index=f"{username}")
    # document_store.delete_documents()
    if extension == "pdf":
        converter = PDFToTextConverter(
            remove_numeric_tables=True, valid_languages=["en"])

        converted_file = converter.convert(
            file_path=filepath, meta={"name": filename})[0]
    elif extension == "docx":
        converter = DocxToTextConverter(
            remove_numeric_tables=False, valid_languages=["en"])
        converted_file = converter.convert(
            file_path=filepath, meta={"name": filename})[0]
    else:
        converter = TextConverter(
            remove_numeric_tables=True, valid_languages=["en"])
        converted_file = converter.convert(
            file_path=filepath, meta={"name": filename})[0]

    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="word",
        split_length=200,
        split_respect_sentence_boundary=True,
        add_page_number=True
    )
    # print(doc_pdf)
    docs_default = preprocessor.process([converted_file])
    print(docs_default)
    # document_store.delete_documents()
    document_store.write_documents(docs_default)

    # document_store.delete_all_documents(index="ahmet", filters=filters)
    # print(document_store.get_all_documents(index="document"))
    # d=document_store.get_documents_by_id([doc_id])


if __name__ == "__main__":
    preprocessor()
