from django.urls import path
from .views import DepositMoneyView, WithdrawView, LoanRequestView, TransactionReportView


urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit"),
    path("withdraw/", WithdrawView.as_view(), name="withdraw"),
    path("loan-request/", LoanRequestView.as_view(), name="loan_request"),
    path("report/", TransactionReportView.as_view(),
         name="transaction_report"),
]
