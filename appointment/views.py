# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from appointment.models import Appointment,AdditionalVisitor
from appointment.AppointmentSerializer import AppointmentSerializer,AdditionalVisitorSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction  #  Import this at top

class BaseAuthentication(viewsets.ViewSet):
    # def list(self, request):
    #     # token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    #     # print(token)  # Token ko print karega
    #     # ... baaki code
    #     return True
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]



class AppointmentCreateView(BaseAuthentication):
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            files = request.FILES

            with transaction.atomic():  #  Start Atomic Transaction
                #  Extract Additional Visitors Data
                additional_visitors = []
                index = 0
                while f"additional_visitor[{index}][name]" in data:
                    additional_visitors.append({
                        "name": data[f"additional_visitor[{index}][name]"],
                        "img": files.get(f"additional_visitor[{index}][img]")  # Handle file upload
                    })
                    index += 1

                #  Create Main Appointment
                appointment_data = Appointment.objects.create(
                    visitor_name=data.get("visitor_name"),
                    email=data.get("email"),
                    phone=data.get("phone"),
                    date=data.get("date"),
                    assigned_to=request.user.gm,
                    company_name=data.get("company_name"),
                    company_address=data.get("company_address"),
                    purpose_of_visit=data.get("purpose_of_visit"),
                    visitor_img=files.get("visitor_img"),
                    created_by=request.user
                )

                #  Prepare Additional Visitors List for Bulk Create
                additional_visitors_list = []
                for visitor in additional_visitors:
                    additional_visitors_list.append(
                        AdditionalVisitor(
                            participants=appointment_data,  # ForeignKey relation
                            name=visitor['name'],
                            img=visitor['img']
                        )
                    )

                #  Bulk Create Additional Visitors
                if additional_visitors_list:
                    AdditionalVisitor.objects.bulk_create(additional_visitors_list)

                print(" Appointment & Visitors Saved Successfully!")

            #  Return success response if everything went fine
            return Response({"message": "Appointment and Additional Visitors created successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(" Error Occurred:", e)
            return Response({"message": "Appointment Not created successfully."}, status=status.HTTP_400_BAD_REQUEST)

# http://127.0.0.1:8000/api/appointments/create-appointment/
# class AppointmentCreateView(viewsets.ModelViewSet):
#     parser_classes = [MultiPartParser, FormParser]

#     def create(self, request, *args, **kwargs):
#         data = request.data.copy()
#         files = request.FILES

#         # Extracting Additional Visitors
#         additional_visitors = []
#         index = 0
#         while f"additional_visitor[{index}][name]" in data:
#             additional_visitors.append({
#                 "name": data[f"additional_visitor[{index}][name]"],
#                 "img": files.get(f"additional_visitor[{index}][img]")  # Handle file uploads
#             })
#             index += 1

#         # Prepare main appointment data
#         appointment_data = {
#             "visitor_name": data.get("visitor_name"),
#             "purpose_of_visit": data.get("purpose_of_visit"),
#             "email": data.get("email"),
#             "phone": data.get("phone"),
#             "company_name": data.get("company_name") or "",
#             "company_address": data.get("company_address") or "kl",
#             "date": data.get("date"),
#             "visitor_img": files.get("visitor_img"),
#             # "created_by": request.user,  #  FIX: Pass UUID instead of user object
#             "additional_visitors": additional_visitors
#         }
        
#         print("🔹 Appointment Data:", appointment_data)  # Debugging

#         # Serialize and save
#         serializer = AppointmentSerializer(data=appointment_data)
#         if serializer.is_valid():
#             appointment = serializer.save()  #  Save main appointment
            
#             #  Save additional visitors separately
#             for visitor_data in additional_visitors:
#                 visitor_data["participants"] = appointment.id  # Link to the appointment
#                 visitor_serializer = AdditionalVisitorSerializer(data=visitor_data)
#                 if visitor_serializer.is_valid():
#                     visitor_serializer.save()
#                 # Process additional visitors after saving
#                 else:
#                     print(" Additional Visitor Error:", visitor_serializer.errors)
#  #  Ek hi email me sabhi ID Cards send karein
#             # send_combined_id_card_email(appointment)

#             return Response(serializer.data, status=status.HTTP_20_CREATED)
        
#         print(" Serializer Errors:", serializer.errors)  # Debugging
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# http://127.0.0.1:8000/api/appointments/get-appointments/?status=PENDING&client=j

class AppointmentListView(BaseAuthentication):
    """
    ViewSet for retrieving appointments with optional filtering.
    Includes related additional visitors.
    """
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        query_params = self.request.GET.dict()
        queryset = Appointment.objects.prefetch_related("additional_visitors").all()  #  Fix here!
        print(queryset)
        for field, value in query_params.items():
            if hasattr(Appointment, field):
                queryset = queryset.filter(**{field: value})
        return queryset

    def get_serializer(self, *args, **kwargs):
        """Manually define `get_serializer()`."""
        return self.serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        print("jj",request.data,request.GET)
        queryset = self.get_queryset()
        # print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# http://127.0.0.1:8000/api/appointments/update-appointments/


class AppointmentUpdateView(BaseAuthentication):
    def create(self, request):
        visitor_id = request.data.get('visitor_id')
        new_description = request.data.get('remark')
        vis_status = request.data.get('status')
        if not visitor_id:
            return Response({'error': 'visitor_id and remark are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            visitor_description = Appointment.objects.get(id=visitor_id)
            visitor_description.description = new_description
            visitor_description.status = vis_status
            visitor_description.save()
            return Response({'success': 'Remark updated successfully'}, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({'error': 'Visitor remark not found'}, status=status.HTTP_404_NOT_FOUND)
        
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







class CallVisitorView(BaseAuthentication):
    def list(self, request):
        visitor_id = request.query_params.get('visitor_id')  # Extract from query
        action = request.query_params.get('action')  # Extract action
        print(visitor_id,action)
        if not visitor_id or not action:
            return Response({'error': 'visitor_id and call field are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            call_visi = Appointment.objects.get(id=visitor_id)
            call_visi.status = action
            call_visi.save()
            return Response({'success': 'calling....'}, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({'error': 'Visitor action not found'}, status=status.HTTP_404_NOT_FOUND)
   









# from django.template.loader import render_to_string
# from weasyprint import HTML
# from django.core.mail import EmailMessage
# from io import BytesIO

# def generate_id_card_pdf(visitor, request):
#     """Bootstrap ke sath ID Card PDF banayein (Using WeasyPrint)"""
#     visitor.img_url = request.build_absolute_uri(visitor.img.url) if visitor.img else None

#     html_string = render_to_string("id_card_template.html", {"visitor": visitor})
#     pdf_io = BytesIO()
    
#     #  Convert HTML to PDF using WeasyPrint
#     HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(pdf_io)
    
#     pdf_io.seek(0)
#     return pdf_io

# def send_combined_id_card_email(appointment, request):
#     """Sirf Additional Visitors ke ID Cards ek hi email me PDF attach karke bhejo"""
#     email_msg = EmailMessage(
#         subject="Your Visitor ID Cards",
#         body=f"Dear {appointment.visitor_name},\n\nHere are the ID cards for all additional visitors.",
#         to=[appointment.email],  #  Ek hi email pe bhejna
#     )

#     #  Additional visitors ke ID cards attach karein
#     for visitor in appointment.additional_visitors.all():
#         pdf = generate_id_card_pdf(visitor, request)  # WeasyPrint PDF generate karega
#         if pdf:
#             email_msg.attach(f"{visitor.name}_ID.pdf", pdf.getvalue(), "application/pdf")

#     email_msg.send()
