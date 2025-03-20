from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import FileUploadSerializer
from .utils import logger


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileUploadSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)

        return Response({'message': f'Uploaded error: {file_serializer.errors}'},
                        status=status.HTTP_400_BAD_REQUEST)