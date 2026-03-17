import json
from django.http import JsonResponse
from .models import MessageLog

def sms_view(request):

    data = json.loads(request.body)

    ho_msg = data.get("wa_ho_msg")

    lines = ho_msg.split("\n")

    name = lines[2].split(":")[1].strip()
    mobile = lines[3].split(":")[1].strip()
    branch = lines[4].split(":")[1].strip()
    document = lines[5].split(":")[1].strip()

    loan = lines[6].split(":")[1].replace("Rs.", "").strip()
    fees = lines[7].split(":")[1].replace("Rs.", "").strip()
    credit = lines[8].split(":")[1].replace("Rs.", "").strip()

    MessageLog.objects.create(
        name=name,
        mobile=mobile,
        branch=branch,
        document=document,
        loan=loan,
        fees=fees,
        credit=credit,
        user=request.user
    )

    return JsonResponse({"status": "success"})