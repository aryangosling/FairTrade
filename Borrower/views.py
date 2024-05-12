import logging
from django.shortcuts import render, redirect
import requests

from .forms import RegisterBorrowerForm
from Lender.models import FairTradeLender


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reg_borrow(request):
    if request.method == "POST":
        form = RegisterBorrowerForm(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.account_type = True
            response = requests.post(
                "http://flask_ml:5000/get_repayment_score",
                json={
                    "education": instance.education,
                    "capital": instance.capital,
                    "income": instance.income,
                    "debt": instance.debt,
                    "interest": instance.interest,
                    "credit_score": instance.credit_score,
                },
            )
            print(response.json())
            try:
                instance.repayment_score = response.json()["repayment_score"]
                instance.save()
                logger.info("Registration successful.")
                return redirect("home_borrow")
            except requests.exceptions.JSONDecodeError:
                logger.warning("Error calculating repayment score!")
    else:
        form = RegisterBorrowerForm()
    return render(request, "Reg_Borrow.html", {"form": form})


def home_borrow(request):
    return render(
        request,
        "Home_Borrow.html",
        {"users_list": FairTradeLender.objects.all().order_by("username")},
    )
