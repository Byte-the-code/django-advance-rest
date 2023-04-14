from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from users.serializers import UserDocumentationUpdateSerializer, UserDocumentationSerializer, UserDocumentationListSerializer
from users.models import UserDocumentation

class UserDocumentationView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if not request.user.is_seller:
            return Response('Only sellers have documentation', status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser:
            return Response('Superusers have no documentation', status=status.HTTP_401_UNAUTHORIZED)
        if request.user.documentation.status == 'not uploaded':
            return Response('Documentation not uploaded yet', status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserDocumentationSerializer(request.user.documentation)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        if not request.user.is_seller:
            return Response('Only sellers have documentation', status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser:
            return Response('Superusers have no documentation', status=status.HTTP_401_UNAUTHORIZED)
        
        if not all(['document_type' in request.data, 'document_identifier' in request.data,
            'front_image' in request.data,'back_image' in request.data]):

            return Response('Missing fields (document_type, document_identifier, front_image, back_image)', status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserDocumentationUpdateSerializer(request.user.documentation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.instance.status = 'uploaded'
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# subject = 'Ecommerce - Documentacion aprobada' if status else 'Ecommerce - Documentacion rechazada'

# if status == True:
#     subject = 'Ecommerce - Documentacion aprobada'
# else:
#     subject = 'Ecommerce - Documentacion rechazada'

class UserDocumentationAdminView(APIView):
    permission_classes = (IsAdminUser,)

    def send_mail(self, user, status, rejected_reason=None):
        html_template = 'documents/user_documentation.html'
        subject = 'Ecommerce - Documentacion aprobada' if status else 'Ecommerce - Documentacion rechazada'
        html_message = render_to_string(html_template, {'name': user.first_name, 'rejected_reason': rejected_reason, 
                                                        'status': status, 'BASE_URL':'localhost:8000' })
        message = EmailMessage(subject, html_message, None, [user.email,]) #use default if 3rd argument is None
        message.content_subtype = 'html'
        message.send()

    def get(self, request):
        users_documents = UserDocumentation.objects.filter(status='uploaded')
        serializer = UserDocumentationListSerializer(users_documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        if not 'document_id' in request.data:
            return Response('Missing document_id', status=status.HTTP_400_BAD_REQUEST)
        
        if not 'status' in request.data or request.data['status'] not in ['approved', 'rejected']:
            return Response('Missing status or status in incorrect', status=status.HTTP_400_BAD_REQUEST)
        
        document_id = request.data['document_id']
        document_status = request.data['status']

        try:
            document = UserDocumentation.objects.get(id=document_id)
        except:
            return Response('Document not found', status=status.HTTP_404_NOT_FOUND)
        
        if document_status == 'rejected':
            if not 'rejected_reason' in request.data:
                return Response('Missing rejected_reason', status=status.HTTP_400_BAD_REQUEST)
            document.rejection_reason = request.data['rejected_reason']
        document.status = document_status
        document.save()

        self.send_mail(document.user, document_status == 'approved', document.rejection_reason)

        return Response('Document status updated', status=status.HTTP_200_OK)
