from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ProtectedView:
    """ 
    Reusable class to protect the routes from unauthorized access.

    Usage Example:
        - class HomeView(ProtectedView, APIView)
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]