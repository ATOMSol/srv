from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from authuser.models import CustomUser
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
import os



def index(request):
    template = "landing/index.html"
    return render(request,template)

class AuthView(View):
    template = "auth/signin.html"

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(phone=identifier)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid phone and password")  # Fix: Pass request
            return redirect("main_server:auth_urls")

        # Authenticate user (Make sure a custom backend supports phone authentication)
        user = authenticate(request, phone=identifier, password=password)
        if user is not None:
            return redirect("main_server:dashboard_urls")

        messages.error(request, "Invalid phone and password")  # Fix: Pass request
        return redirect("main_server:auth_urls")
    


class LogoutView(View):
    def get(self, request):
        logout(request)  # Logs out the user
        return redirect("/")  # Redirect to login page

class Dashboard(View):
    template = "dashboard/dashboard_home.html"
    def get(self,request):
        gm_count = CustomUser.objects.filter(groups__name="GM").count()
        pa_count = CustomUser.objects.filter(groups__name="PA").count()
        active_users = CustomUser.objects.filter(is_active=True).count()
        context = {
            "gm_count": gm_count,
            "pa_count": pa_count,
            "active_users": active_users
        }
        return render(request,self.template, context)


        

class UserListView(View):
    template = "dashboard/user/user_list.html"
    model_name=CustomUser
    # roles="gm"
    group_name="GM"

    def get(self, request):
        data_users=self.model_name.objects.filter(groups__name=self.group_name)
        gm_list = self.model_name.objects.filter(groups__name="GM").distinct()
        return render(request, self.template,{"data_users":data_users,"roles":self.group_name,"gm_list":gm_list,"main_server_api": os.getenv("MAIN_SERVER_DOMAIN"),})
    
class GmList(UserListView):...

class PaList(UserListView):
    # template = "dashboard/pa/user_list.html"
    # model_name=CustomUser
    # roles="pa"
    group_name="PA"





class AddUserView(View):
    template = "dashboard/user/add_user.html"
    model_name=CustomUser
    # roles="gm"
    group_name="GM"
    def get(self, request):
        # data_users=self.model_name.objects.filter(roles__name=self.roles)
        gm_list = self.model_name.objects.filter(groups__name='GM').distinct()
        # gm_list = self.model_name.objects.filter(groups__name='GM').values('first_name', 'last_name', 'unique_id').distinct()


        return render(request, self.template,{"gm_list":gm_list,"roles":self.group_name})
    
    def post(self,request):
        if request.method == "POST":
         
            if self.model_name.objects.filter(phone=request.POST.get("phone")).exists():
                messages.info(request,"Already Exists")
                return redirect("main_server:dashboard_urls")
            # Create the user
            user = self.model_name.objects.create(phone=request.POST.get("phone"), first_name=request.POST.get("first_name"), last_name=request.POST.get("last_name"), email=request.POST.get("email"),password=make_password(request.POST.get("password")))
           
            # Assign role
            # role_name = self.roles
            # print("role.........................",role_name)
            # role = Role.objects.get(name=role_name)
            # user.roles.add(role)

            # Assign GM if selected
            # if request.POST.get("gm"):
            #     gm_user = self.model_name.objects.get(unique_id=request.POST.get("gm"))
            #     user.gm = gm_user
            #     user.save()

    
            group = Group.objects.get(name=self.group_name)
            user.groups.add(group)
        messages.success(request,"Add User Successfull !")
        return redirect("main_server:dashboard_urls")


class GmAddUser(AddUserView):...

class PaAddUser(AddUserView):
    # template = "dashboard/pa/user_list.html"
    # model_name=CustomUser
    # roles="pa"
    group_name="PA"






class UpdateUser(View):
    def post(self,request):
        if request.method == "POST":
            user_id = request.POST.get("user_id")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            # role = request.POST.get("role")
        

            user = get_object_or_404(CustomUser, unique_id=user_id)
            user.first_name = first_name
            user.last_name = last_name
           
           
            # selected_role = request.POST.get('role')  # Get a single role name as a string
            # print("Selected role:", selected_role)  # Debugging output

            # if selected_role:  # Ensure a role was selected
            #     try:
            #         role_object = Role.objects.get(name=selected_role)  # Get the Role object
            #         user.roles.set([role_object])  # Update the user's role (set expects a list)
            #     except Role.DoesNotExist:
            #         print("Error: Role does not exist")  # Handle missing role gracefully


            group_change=request.POST.get('role')
            if group_change:  # Ensure role is not None
                group = Group.objects.get(name=group_change.upper())
                user.groups.clear()  # Remove previous group
                user.groups.add(group)

            if request.POST.get("gm"):
                user.gm_id = request.POST.get("gm") if request.POST.get("gm") else None
            user.save()

            messages.success(request, "User updated successfully!")
            return redirect("main_server:dashboard_urls")  # Change this to your user list view

        messages.error(request, "Invalid request.")
        return redirect("main_server:dashboard_urls")





import json
from django.http import JsonResponse
from authuser.models import CustomUser

class Passkey(View):
    def post(self, request):
        try:
            print(request.POST)
            unique_id = request.POST.get("unique_id")  # Get user ID from JSON request
            pass_key = request.POST.get("pass_key")  # Get passkey

            if not unique_id or not pass_key:
                return JsonResponse({"error": "Missing unique_id or pass_key"}, status=400)

            user = CustomUser.objects.get(phone=unique_id)
            user.pass_key = pass_key
            user.save()

            # messages.success(request, "Passkey added successfully")
            return JsonResponse({"message": "Passkey saved successfully!"}, status=200)

        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"Something went wrong: {str(e)}"}, status=500)
    