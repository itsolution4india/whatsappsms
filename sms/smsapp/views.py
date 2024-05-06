# import requests # type: ignore
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser
from io import BytesIO
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm
from decimal import Decimal

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .campaignmail import send_email_change_notification
import logging
from .models import ReportInfo,CampaignData
from django.contrib.auth import logout
import requests

# Logger setup for logging information, warnings, or errors.
logger = logging.getLogger(__name__)
from datetime import datetime


# View for user login
def user_login(request):
    from .forms import UserLoginForm  # Assuming form is in the same app

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                logger.info(f"User {email} logged in successfully.")
                return redirect("dashboard")
            else:
                # Authentication failed
                logger.warning(f"Failed login attempt for email: {email}")
                form.add_error(None, "Invalid email or password.")
        else:
            logger.warning(f"Invalid form submission: {form.errors}")

    else:
        form = UserLoginForm()

    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login.hml")

@login_required
def user_dashboard(request):
    return render(request, "dashboard.html")


# View for file upload page
@login_required
def Send_Sms(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            ip_address = request.META.get("REMOTE_ADDR", "Unknown IP")
            coins = request.user.coins
            report_list = ReportInfo.objects.filter(email=request.user)
            campaign_list = CampaignData.objects.filter(email=request.user)
            new_message_info = None

            template_id = request.POST.get("params")
            uploaded_file = request.FILES.get("files")

            if not uploaded_file:
                error_message = "No file was uploaded"
                return render(
                    request,
                    "send-sms.html",
                    {
                        "error_message": error_message,
                        "ip_address": ip_address,
                        "coins": coins,
                        "report_list": report_list,
                        "campaign_list":campaign_list,
                    },
                )

            try:
                file_content = uploaded_file.read()
                final_count,contact_list=remove_duplicate_and_invalid_contacts(file_content)
                url = "http://192.168.29.2000:3000/send_messages/"
                api_response = requests.post(url, json={"template_id": template_id, "contact_list": contact_list})

                if api_response.status_code == 200:
                    success_message = api_response.json()
                    subtract_coins(request, final_count)
                    new_message_info = ReportInfo(
                        email=request.user,
                        message_date=datetime.now(),
                        message_delivery=final_count,
                        message_send=final_count,
                        message_failed=2,
                    )
                    new_message_info.save()
                    print("New row added successfully!")
                    # Set session variable to indicate coins deduction
                    request.session["coins_deducted"] = True
                    return render(
                        request,
                        "send-sms.html",
                        {
                            "success_message": success_message,
                            "ip_address": ip_address,
                            "coins": coins,
                            "report_list": report_list,
                            "campaign_list":campaign_list,
                        },
                    )
                else:
                    error_message = f"API request failed with status code: {api_response.status_code}"
                    return render(
                        request,
                        "send-sms.html",
                        {
                            "error_message": error_message,
                            "ip_address": ip_address,
                            "coins": coins,
                            "report_list": report_list,
                            "campaign_list":campaign_list,
                        },
                    )
            except requests.RequestException as e:
                error_message = f"Error occurred during API request: {e}"
                return render(
                    request,
                    "send-sms.html",
                    {
                        "error_message": error_message,
                        "ip_address": ip_address,
                        "coins": coins,
                        "report_list": report_list,
                        "campaign_list":campaign_list,
                    },
                )

        else:
            ip_address = request.META.get("REMOTE_ADDR", "Unknown IP")
            coins = request.user.coins
            report_list = ReportInfo.objects.filter(email=request.user)
            campaign_list = CampaignData.objects.filter(email=request.user)
            return render(
                request,
                "send-sms.html",
                {
                    "ip_address": ip_address,
                    "coins": coins,
                    "report_list": report_list,
                    "campaign_list":campaign_list,
                },
            )
    else:
        return redirect("login")


# Password Reset Method
def initiate_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            send_otp(email)
            return redirect("otp_verification", email=email, token=token)
        except ObjectDoesNotExist:
            return render(
                request,
                "password_reset.html",
                {"error_message": "Email does not exist"},
            )
    return render(request, "password_reset.html")


def verify_otp(request, email, token):
    if request.method == "POST":
        otp = request.POST.get("otp")
        if verify_otp_server(otp):
            return redirect("change_password", email=email, token=token)
        else:
            return render(
                request, "otp_verification.html", {"error_message": "Invalid OTP"}
            )
    return render(request, "otp_verification.html")


def change_password(request, email, token):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")
        if new_password == confirm_new_password:
            try:
                user = CustomUser.objects.get(email=email)
                if default_token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    return redirect("login")
                else:
                    return render(
                        request,
                        "change_password.html",
                        {"error_message": "Invalid or expired token"},
                    )
            except ObjectDoesNotExist:
                return render(
                    request,
                    "change_password.html",
                    {"error_message": "Email does not exist"},
                )
        else:
            return render(
                request,
                "change_password.html",
                {"error_message": "Passwords do not match"},
            )
    return render(request, "change_password.html")


def verify_otp_server(otp):
    verify_otp_url = "http://13.239.113.104/email/verify_otp"
    params = {"otp": otp}
    verify_otp_response = requests.post(verify_otp_url, params=params)
    return verify_otp_response.status_code == 200


def send_otp(email):
    otp_url = "http://13.239.113.104/email/otp"
    params = {"name": "otp", "email": email}
    otp_response = requests.post(otp_url, params=params)

    if otp_response.status_code == 200:
        print("OTP sent successfully.")
    else:
        return redirect("password_reset.html")


#Valid _and _ Duplicate method
import re

def validate_phone_number(phone_number):
    
    pattern = re.compile(r'^(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
    return bool(pattern.match(phone_number))



def remove_duplicate_and_invalid_contacts(file_path):

    unique_valid_contacts = set()
  

    
    with open(file_path, 'r') as file:
        for line in file:
            phone_number = line.strip()

            if validate_phone_number(phone_number):
                unique_valid_contacts.add(phone_number)
            else:
                continue
                #print(f"Warning: Invalid phone number '{phone_number}' found and skipped.")
    return len(unique_valid_contacts),list(unique_valid_contacts)
        




from django.contrib import messages


@login_required
def subtract_coins(request, final_count):
    # Retrieve the current logged-in user
    user = (
        request.user
    )  # No need to use get_object_or_404 because request.user is already the authenticated user

    # Calculate the amount of coins to subtract based on final_count
    final_coins = Decimal(final_count) * Decimal("0.10")

    # Check if the user has enough coins to proceed
    if user.coins >= final_coins:
        # Subtract the coins and save the user object
        user.coins -= final_coins
        user.save()

        # Provide feedback to the user about the successful transaction
        messages.success(
            request, f"Successfully subtracted {final_coins} coins from your account."
        )
    else:
        # Notify the user that they do not have enough coins
        messages.error(request, "You don't have enough coins to proceed.")


@login_required
def Campaign(request):
    campaign_list = CampaignData.objects.filter(email=request.user)
    if request.method == 'POST':

        template_id = request.POST.get('template_id')
        sub_service = request.POST.get('sub_service')
        template_data = request.POST.get('template_data')
        text = request.FILES.get("text")
        image = request.FILES.get("image")
        video = request.FILES.get("video")
        pdf = request.FILES.get("pdf")

        CampaignData.objects.create(email=request.user,template_id=template_id,sub_service=sub_service,template_data=template_data,text=text, image=image, video=video, pdf=pdf)
        email=request.user
        print(email)
        send_email_change_notification(email, template_id)
        campaign_list = CampaignData.objects.filter(email=request.user)
        return render(request, "Campaign.html",{"campaign_list": campaign_list})
    return render(request, "Campaign.html",{"campaign_list": campaign_list})


@login_required
def Reports(request):
    report_list = ReportInfo.objects.filter(email=request.user)
    return render(request, 'reports.html', {"report_list":report_list})


