from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import TransactionModel
from django.views.generic import CreateView, ListView
from .constants import DEPOSIT, WITHDRAWAL, LOAN
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DepositForm, WithdrawForm, LoanRequestForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum
# Create your views here.


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = "transactions/transaction_form.html"
    model = TransactionModel
    success_url = reverse_lazy("transaction_report")
    title = ""

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "account": self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": self.title
        })
        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(self.request, f'{"{:,.2f}".format(
            float(amount))}$ was deposited to your account successfully')

        return super().form_valid(form)


class WithdrawView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = "Withdraw"

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance -= amount
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(self.request, f'{"{:,.2f}".format(
            float(amount))}$ was withdrawn to your account successfully')

        return super().form_valid(form)


class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = "Request For Loan"

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        loan_count = TransactionModel.objects.filter(
            account=account, transaction_type=LOAN, loan_approve=True).count()

        if loan_count >= 3:
            return HttpResponse("You have cross the loan limits")

        messages.success(
            self.request,
            f'Loan request for {"{:,.2f}".format(
                float(amount))}$ submitted successfully'
        )
        return super().form_valid(form)


class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = "transactions/transaction_report.html"
    title = "Transactions"
    balance = 0
    model = TransactionModel

    def get_queryset(self):
        queryset = super().get_queryset().filter(account=self.request.user.account)

        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = queryset.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date)

            self.balance = TransactionModel.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context
