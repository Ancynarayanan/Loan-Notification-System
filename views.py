import json
import os
from django.http import JsonResponse

from twilio.rest import Client

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.db.models import Count
from .models import MessageLog

# -----------------------------
# 🏠 Home Page
# -----------------------------
def home(request):
    return render(request, "home.html")



# Admin Login
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:  # Only admins
            login(request, user)
            return redirect("admin_dashboard")
        else:
            return render(request, "admin_login.html", {"error": "Invalid admin credentials"})

    return render(request, "admin_login.html")



# -----------------------------
# 🏢 Admin Dashboard
# -----------------------------
@staff_member_required
def admin_dashboard(request):
    today = timezone.now().date()

    today_reports = MessageLog.objects.filter(created_at__date=today)
    today_count = today_reports.count()

    month_count = MessageLog.objects.filter(
        created_at__month=today.month
    ).count()

    total_count = MessageLog.objects.count()

    branch_data = MessageLog.objects.values("branch").annotate(
        total=Count("branch")
    )

    context = {
        "today_reports": today_reports,
        "today_count": today_count,
        "month_count": month_count,
        "total_count": total_count,
        "branch_data": branch_data
    }

    return render(request, "admin-dashboard.html", context)

# Admin Logout
def logout_admin(request):
    if request.user.is_authenticated and request.user.is_staff:
        logout(request)
    return redirect('admin_login')


# Team Login
# -----------------------------
# 👨‍💼 Team Login
# -----------------------------
def team_login(request):
    # Already loginனா → sms_page
    if request.user.is_authenticated:
        return redirect("sms_page")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("sms_page")
        else:
            return render(request, "team_login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "team_login.html")


# Team Logout
def logout_team(request):
    if request.user.is_authenticated and not request.user.is_staff:
        logout(request)
    return redirect('team_login')
# -----------------------------
# 📩 SMS Page (Team Only)
# -----------------------------
@login_required
def sms_page(request):
    return render(request, "index.html")


# Twilio Credentials from environment
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")          # SMS sending number
WHATSAPP_FROM = os.getenv("WHATSAPP_FROM")        # Live WhatsApp sender
HEAD_OFFICE_NO = os.getenv("HEAD_OFFICE_NO")      # Head office number (just digits, no +91)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@login_required
def send_sms_whatsapp(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)

        mobile = data.get("mobile")
        template_vars = data.get("template_variables")
        sms_tamil = data.get("sms_tamil")

        if not mobile or not template_vars or len(template_vars) < 8:
            return JsonResponse({"error": "Mobile and template variables required"}, status=400)

        # ----------------------------
        # Sanitize numbers
        # ----------------------------
        mobile = ''.join(filter(str.isdigit, mobile))  # remove any + or spaces
        wa_to = f"whatsapp:+91{mobile}"
        ho_to = f"whatsapp:+91{HEAD_OFFICE_NO}"

        # ----------------------------
        # 1️⃣ Send SMS to client
        # ----------------------------
        sms_client = None
        if sms_tamil:
            sms_client = client.messages.create(
                body=sms_tamil,
                from_=TWILIO_PHONE,
                to=f"+91{mobile}"
            )

        # ----------------------------
        # 2️⃣ Send WhatsApp template to client
        # ----------------------------
        wa_client = client.messages.create(
            from_=WHATSAPP_FROM,
            to=wa_to,
            content_sid="HX5814ee1fc320b0e5b4ecc643027ba607",  # approved template SID
            content_variables=json.dumps({
            "1": template_vars[0],  # nameTamil
            "2": template_vars[1],  # name (English)
            "3": template_vars[2],  # document
            "4": template_vars[3],  # branch
            "5": template_vars[4],  # fees
            "6": template_vars[5],  # phone
            "7": template_vars[6],  # email
            "8": template_vars[7]  # map
            })
        )

        # ----------------------------
        # 3️⃣ Send WhatsApp to Head Office
        # ----------------------------

        wa_ho = client.messages.create(
            from_=WHATSAPP_FROM,
            to=ho_to,
            content_sid="HXc178e75d6743c17448488e9dbc172fe7",
            content_variables=json.dumps({
                "1": template_vars[1],  # name English
                "2": mobile,
                "3": template_vars[3],  # branch
                "4": template_vars[2],  # document
                "5": data.get("loan"),
                "6": template_vars[4],  # fees
                "7": data.get("credit"),
                "8": template_vars[6],  # email
                "9": template_vars[7]  # map
            })
        )

        return JsonResponse({
            "status": "success",
            "client_sms_sid": sms_client.sid if sms_client else None,
            "client_wa_sid": wa_client.sid,
            "ho_wa_sid": wa_ho.sid
        })

    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)})