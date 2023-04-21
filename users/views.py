from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db.models import Q, Count, Value, CharField
from django.template.loader import render_to_string
from django.db.models.functions import Concat
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.conf import settings

from users.serializers import UserDocumentationUpdateSerializer, UserDocumentationSerializer, \
    UserDocumentationListSerializer, UserListSerializer, SellerListSerializer
from users.models import UserDocumentation, User

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


class UserListView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = User.objects.all()

        if 'is_active' in request.query_params:
            users = users.filter(is_active = request.query_params['is_active'])

        if 'user_type' in request.query_params:
            user_type = request.query_params['user_type']
            if user_type not in ['buyer', 'seller']:
                return Response({'error':'user_type must be buyer or seller'},
                    status=status.HTTP_400_BAD_REQUEST)
            users = users.filter(user_type = user_type)
        
        if 'search' in request.query_params:
            # users = users.filter(
            #     Q(first_name__icontains = request.query_params['search']) | # | = or
            #     Q(last_name__icontains = request.query_params['search']) |
            #     Q(email__icontains = request.query_params['search'])
            #     )

            users = (users.annotate(full_search_field = Concat('first_name', 
                                                            Value(' '),'last_name', 
                                                            Value(' '),'email',
                                                            Value(' '),'last_name', 
                                                            Value(' '),'first_name', 
                                                            output_field = CharField()))
                .filter(full_search_field__icontains = request.query_params['search']))
        
        if 'order_by' in request.query_params:
            order_by = request.query_params['order_by']
            
            prefix = ''
            if order_by[0] == '-':
                prefix = '-'
                order_by = order_by[1:]

            if order_by not in ['id', 'first_name', 'last_name', 'email', 'profile__birth_date']:
                return Response({'error':'order_by must be first_name, last_name, email or profile__birth_date'},
                                status=status.HTTP_400_BAD_REQUEST)

            users = users.order_by(prefix + order_by)
    
        per_page = request.query_params.get('per_page', 5)
        page = int(request.query_params.get('page', 1))
        paginator = Paginator(users, per_page)
        data = paginator.page(page)

        serializer = UserListSerializer(data, many=True)
        
        return Response({
            'page':page,
            'total_items':len(users),
            'total_pages':paginator.num_pages,
            'data':serializer.data}, status=status.HTTP_200_OK)

class SellersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if request.user.is_staff:
                if 'document_status' in request.query_params:
                    sellers = (User.objects.filter(
                                user_type = 'seller',
                                documentation__status = request.query_params['document_status'])
                                .order_by('id'))
                else:
                    sellers = User.objects.filter(user_type = 'seller').order_by('id')
            else:
                sellers = User.objects.filter(
                            user_type = 'seller',
                            documentation__status = 'Approved').order_by('id')

            # sellers = sellers.annotate(products_count = Count('products'))

            if 'search' in request.query_params:
                search = request.query_params['search']
                sellers = sellers.annotate(search_field = Concat(
                                    'first_name', Value(' '), 
                                    'last_name', Value(' '), 
                                    'email', Value(' '),
                                    output_field = CharField())).filter(search_field__icontains = search)
            per_page = request.query_params.get('per_page', 5)
            page = request.query_params.get('page', 1)
            paginator = Paginator(sellers, per_page)
            data = paginator.page(page)

            serializer = SellerListSerializer(data, many=True)

            return Response({'page':page, 'total_pages':paginator.num_pages, 
                        'total_items':sellers.count(), 'data':serializer.data},
                        status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'errors':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)