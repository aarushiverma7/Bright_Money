from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserRegistrationSerializer
from .tasks import calculate_credit_score_task

# Create a class of RegisterUserAPIView having a unique user id

class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            calculate_credit_score_task.delay(user.aadhar_id)
            return Response({
                "error": None,
                "unique_user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
