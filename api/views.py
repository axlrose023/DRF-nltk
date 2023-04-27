from .serializers import ApiSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .nltk import NounPhraseExtractor, TreeTextRetriever


@api_view(['GET'])
def tree_view(request):
    serializer = ApiSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    tree = serializer.validated_data['tree']
    limit = int(request.query_params.get('limit', 20))
    retriever = TreeTextRetriever(tree)
    text = retriever.get_text()
    extractor = NounPhraseExtractor(tree=tree, text=text)
    result = extractor.extract_noun_phrases()
    result = result['paraphrases'][:limit]
    return Response({'paraphrases': result})
