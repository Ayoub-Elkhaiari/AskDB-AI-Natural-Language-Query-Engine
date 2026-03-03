import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.schema_service import extract_postgres_schema, extract_mongo_schema
from services.llm_service import generate_query
from services.security_service import validate_query
from services.query_service import execute_postgres, execute_mongo

logger = logging.getLogger(__name__)


class GenerateQueryView(APIView):
    def post(self, request):
        database = request.data.get('database')
        question = request.data.get('question', '').strip()

        if database not in ['postgres', 'mongo']:
            return Response({'error': 'database must be postgres or mongo'}, status=status.HTTP_400_BAD_REQUEST)
        if not question:
            return Response({'error': 'question is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            schema = extract_postgres_schema() if database == 'postgres' else extract_mongo_schema()
            generated = generate_query(database, schema, question)
            return Response({'schema': schema, 'generated_query': generated})
        except Exception as exc:
            logger.exception('Failed to generate query')
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExecuteQueryView(APIView):
    def post(self, request):
        database = request.data.get('database')
        query = request.data.get('query', '').strip()

        if database not in ['postgres', 'mongo']:
            return Response({'error': 'database must be postgres or mongo'}, status=status.HTTP_400_BAD_REQUEST)
        if not query:
            return Response({'error': 'query is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_query(database, query)
            results = execute_postgres(query) if database == 'postgres' else execute_mongo(query)
            return Response({'results': results})
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.exception('Failed to execute query')
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
