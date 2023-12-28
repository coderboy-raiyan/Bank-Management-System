from django.urls import path
from .views import DepositMoneyView, WithdrawView, LoanRequestView, TransactionReportView, LoanListView, PayLoanView


urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit"),
    path("withdraw/", WithdrawView.as_view(), name="withdraw"),
    path("loan-request/", LoanRequestView.as_view(), name="loan_request"),
    path("loans/", LoanListView.as_view(), name="loan_list"),
    path("report/", TransactionReportView.as_view(),
         name="transaction_report"),
    path("loans/<int:loan_id>/", PayLoanView.as_view(), name="pay"),
]
