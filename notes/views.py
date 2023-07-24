from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
import jwt
from .models import Note
from .serializers import NoteSerializer
from rest_framework import status


class NoteAPIView(APIView):
    def verify_token(self, request):
        # Get the token from the Authorization header
        token = request.META.get('HTTP_AUTHORIZATION', '')
        # secret_key = 'your_secret_key_here'  # Replace this with your actual secret key used for token encoding
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            request.user = payload  # Set the decoded payload as the user for the request
            return True
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")


    def get(self, request, pk=None):
        print(request)
        if not self.verify_token(request):
            raise AuthenticationFailed(
                "Authentication credentials were not provided.")
    
        if pk is None:
            notes = Note.objects.filter(user=request.user['id'])
            if not notes:
                
                print('hheh')
                return Response({"message": "Notes not found."}, status=status.HTTP_404_NOT_FOUND)
    
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)

        try:
            note = Note.objects.get(pk=pk, user=request.user['id'])
            serializer = NoteSerializer(note)
      

            return Response(serializer.data)
    
        except Note.DoesNotExist:
            raise NotFound("Note not found.")

    def post(self, request):
        if not self.verify_token(request):
            raise AuthenticationFailed(
                "Authentication credentials were not provided.")
        
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Set the user ID from the token payload
        serializer.save(user_id=request.user['id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        if not self.verify_token(request):
            raise AuthenticationFailed(
                "Authentication credentials were not provided.")

        try:
            # If the 'pk' parameter is provided, retrieve the specific note by its primary key
            note = Note.objects.get(pk=pk, user=request.user['id'])
        except Note.DoesNotExist:
            raise NotFound("Note not found.")

        serializer = NoteSerializer(note, data=request.data)
        serializer.is_valid(raise_exception=True)
        # Ensure the user is the owner of the note
        serializer.save(user_id=request.user['id'])
        return Response(serializer.data)

    def delete(self, request, pk=None):
        if not self.verify_token(request):
            raise AuthenticationFailed(
                "Authentication credentials were not provided.")

        try:
            # If the 'pk' parameter is provided, retrieve the specific note by its primary key
            note = Note.objects.get(pk=pk, user=request.user['id'])
        except Note.DoesNotExist:
            raise NotFound("Note not found.")

        note.delete()
        return Response({"message": "Note deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
