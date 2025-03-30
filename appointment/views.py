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
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



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

                print(" Appointment & Visitors Saved Successfully!",additional_visitors_list)
            mail(appointment_data.visitor_name,appointment_data.email,appointment_data.date,f"{request.user.gm.first_name} {request.user.gm.last_name}",additional_visitors_list,"Appointment Confirmation","message")
            #  Return success response if everything went fine
            return Response({"message": "Appointment and Additional Visitors created successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(" Error Occurred:", e)
            return Response({"message": "Appointment Not created successfully."}, status=status.HTTP_400_BAD_REQUEST)
        

# {'id': '6f340447-cedd-49f5-9fc3-550124b0be2b', 
#  'visitor_img': 'https://i.pinimg.com/474x/0a/a8/58/0aa8581c2cb0aa948d63ce3ddad90c81.jpg', 
#  'additional_visitors': [], 'visitor_name': 'K', 'email': 'k@fk.in', 'phone': '7481253621',
#    'date': '2025-03-29', 'description': '', 'status': 'pending', 'company_name': 'G', 'company_address': 'KK',
#      'purpose_of_visit': 'K', 'created_at': '2025-03-29T04:14:55.906687+05:30', 'updated_at': '2025-03-29T04:14:55.906687+05:30', 
#      'assigned_to': '3ac08101-993f-4b58-8baf-7d07b4a964d6', 'created_by': 'bf922f51-1a4f-441d-9510-3e5b021f7fbc', 'updated_by': None}


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
        # print(queryset)
        for field, value in query_params.items():
            if hasattr(Appointment, field):
                queryset = queryset.filter(**{field: value})
        return queryset

    def get_serializer(self, *args, **kwargs):
        """Manually define `get_serializer()`."""
        return self.serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        # print("jj",request.data,request.GET)
        queryset = self.get_queryset()
        # print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# http://127.0.0.1:8000/api/appointments/update-appointments/


class AppointmentUpdateView(BaseAuthentication):
    def create(self, request):
        visitor_id = request.data.get('visitor_id')
        new_description = request.data.get('remark')
        if not visitor_id:
            return Response({'error': 'visitor_id and remark are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            visitor_description = Appointment.objects.get(id=visitor_id)
            visitor_description.description = new_description
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
        # print(visitor_id,action)
        if not visitor_id or not action:
            return Response({'error': 'visitor_id and call field are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            call_visi = Appointment.objects.get(id=visitor_id)
            call_visi.status = action
            call_visi.save()
            return Response({'success': 'calling....'}, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({'error': 'Visitor action not found'}, status=status.HTTP_404_NOT_FOUND)
   










def mail(visitor_name,client_email,date,gm,additional_visitors,subject,message):
    print("ad",additional_visitors)
    try:
        from_email = "mastikipathshala828109@gmail.com"
        
        # Correct template_path and render the HTML template with the provided data
        template_path = 'mail_templates/appointment-confirmation-email.html'
        context = {
            'visitor_name': visitor_name,
            'message':message,
            'client_email':client_email,
            'date':date,
            'gm':gm,
            'additional_visitors':additional_visitors,
        }
        
        # Render the HTML template to a string
        message = render_to_string(template_path, context)
        
        to = client_email
        
        # Create an email message object and attach the HTML message
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(message, 'text/html')
        try:
            print("Sdfsd")
            msg.send()
        except Exception as e:
            print("Error sending email:", e)
            raise Exception("Problem sending email check password")
        
    except Exception as e:
        print("Error sending email:", e)
        raise Exception("Problem sending email")



# def AppointmentCreateMail(self,request):