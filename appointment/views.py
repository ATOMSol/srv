# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from appointment.models import Appointment,AdditionalVisitor
from appointment.AppointmentSerializer import AppointmentSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class BaseAuthentication(viewsets.ViewSet):
    # def list(self, request):
    #     # token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    #     # print(token)  # Token ko print karega
    #     # ... baaki code
    #     return True
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class AppointmentCreateView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        print(request.data)  # Debugging

        # Convert request data to a mutable dictionary
        data = request.data.copy()

        # Handle visitor image separately
        if 'visitor_img' in request.FILES:
            data['visitor_img'] = request.FILES['visitor_img']

        # Process additional visitors correctly
        additional_visitors = []
        index = 0
        while f'additional_visitors[{index}][name]' in request.data:
            visitor_data = {
                'name': request.data.get(f'additional_visitors[{index}][name]'),
                'img': request.FILES.get(f'additional_visitors[{index}][img]')
            }
            additional_visitors.append(visitor_data)
            index += 1

        # Add additional visitors to request data
        data['additional_visitors'] = additional_visitors

        # Serialize and validate data
        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user, assigned_to=request.user.gm if hasattr(request.user, "gm") else None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# http://127.0.0.1:8000/api/appointments/create-appointment/

# class AppointmentCreateView(viewsets.ModelViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]

#     def create(self, request, *args, **kwargs):
#         print(request.data)   # Debugging
#         print(request.FILES)  # Debugging for file uploads

#         # Convert request data to a mutable dictionary
#         data = request.data.copy()  # Copy to make it mutable

#         # Handle visitor image separately
#         if 'visitor_img' in request.FILES:
#             data['visitor_img'] = request.FILES['visitor_img']

#         # Extract additional visitors
#         additional_visitors = []
#         index = 0
#         while f'additional_visitor[{index}][name]' in request.data or f'additional_visitor[{index}][img]' in request.FILES:
#             visitor_data = {
#                 'name': request.data.get(f'additional_visitor[{index}][name]', None),  # Extract name safely
#                 'img': request.FILES.get(f'additional_visitor[{index}][img]', None)  # Extract image safely
#             }
#             additional_visitors.append(visitor_data)

#             # Remove extracted keys from `data`
#             data.pop(f'additional_visitor[{index}][name]', None)  # Use `.pop()` to avoid KeyError
#             data.pop(f'additional_visitor[{index}][img]', None)  # Use `.pop()` for safety

#             index += 1

#         # print("Cleaned Data:", data)  # Debugging
#         # print("Extracted Additional Visitors:", additional_visitors)  # Debugging
#     # Create Appointment first
#         appointment = Appointment.objects.create(
#             visitor_name=data.get("visitor_name"),
#             email=data.get("email"),
#             phone=data.get("phone"),
#             date=data.get("date"),
#             company_name=data.get("company_name"),
#             company_address=data.get("company_adress"),
#             purpose_of_visit=data.get("purpose_of_visit"),
#             visitor_img=data.get("visitor_img"),
#             created_by=request.user,
#             assigned_to=request.user.gm if hasattr(request.user, "gm") else None
#         )        
#         # Create Additional Visitors
#         for visitor in additional_visitors:
#             AdditionalVisitor.objects.create(
#                 participants=appointment,  # Link to the created Appointment
#                 name=visitor["name"],
#                 img=visitor["img"]
#             )
#         return Response({"message": "Appointment created successfully!"}, status=201)

#         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# http://127.0.0.1:8000/api/appointments/get-appointments/?status=PENDING&client=j
class AppointmentListView(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        # Get all query parameters
        query_params = request.GET.dict()  # Convert QueryDict to a dictionary
        # print(query_params)
        # Start with the base queryset
        queryset = Appointment.objects.all()
        # print(queryset)
        # Loop through query parameters and apply filters
        for field, value in query_params.items():
            if hasattr(Appointment, field):  # Check if the field exists in the model
                queryset = queryset.filter(**{field: value})
        
        # Serialize the filtered queryset
        serializer = AppointmentSerializer(queryset, many=True)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

# http://127.0.0.1:8000/api/appointments/update-appointments/

class AppointmentUpdateView(BaseAuthentication):
    """
    Update an existing appointment.
    """
    def patch(self, request: object) -> Response:
        pk = request.GET.get("pk")
        if not pk:
            return Response({"error": "Missing 'pk' parameter"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pk = int(pk)
        except ValueError:
            return Response({"error": "Invalid 'pk' parameter"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAppointmentView(BaseAuthentication):
    """
    Delete an existing appointment.
    """
    def list(self, request):
        if not request.GET.get("visitorId"):
            return Response({"error": "Missing 'id' parameter"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            appointment = Appointment.objects.get(id=request.GET.get("visitorId"))
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        appointment.delete()
        return Response({"message": "Appointment deleted successfully"}, status=status.HTTP_200_OK)
