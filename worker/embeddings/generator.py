from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

def getEmbeddingsPerChunck(chunks: list[str]) -> list[list[float]]:
    allEmbedings = []

    for chunk in chunks:
        model = TextEmbeddingModel.from_pretrained("text-embedding-004")

        text_input = TextEmbeddingInput(
            text=chunk,
            task_type="RETRIEVAL_DOCUMENT"
        )

        embeddings = model.get_embeddings([text_input])
        allEmbedings.append(embeddings[0].values)

    return allEmbedings
