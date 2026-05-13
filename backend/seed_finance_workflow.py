#!/usr/bin/env python
"""
Dedicated seed script for financing workflow samples.
Creates finance users, products, applications, loans, repayments,
investor profiles, agreements, bank accounts, and settlements.

Safe to rerun independently; all writes are idempotent.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from finance.models import (
    FinanceProduct,
    FinanceApplication,
    FinanceLoan,
    FinanceRepayment,
    SupplierCreditLine,
)
from banking.models import BankAccount, SettlementTransaction
from regulation.models import InvestorProfile, InvestmentAgreement
from escrow.models import EscrowAccount, EscrowTransaction

User = get_user_model()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', stream=sys.stdout)


def log_seed_banner(title):
    logger.info("=" * 60)
    logger.info(title)
    logger.info("=" * 60)


def log_seed_result(label, identifier, created):
    action = "created" if created else "updated"
    logger.info(f"✅ {label} {action}: {identifier}")


def ensure_finance_users():
    """Create or update finance-specific demo users."""
    # Finance Officer (approves loans, manages disbursements)
    finance_officer, created = User.objects.update_or_create(
        username='finance_officer',
        defaults={
            'email': 'finance@ujenzi.com',
            'role': User.Role.PROJECT_OWNER,
            'first_name': 'Finance',
            'last_name': 'Officer',
            'is_staff': False,
            'is_superuser': False,
        },
    )
    finance_officer.set_password('password123')
    finance_officer.save(update_fields=['password'])
    # Assign finance officer custom role if supported by your RBAC
    if hasattr(finance_officer, 'grant_role'):
        finance_officer.grant_role('FINANCE_OFFICER')
        finance_officer.sync_groups()
    log_seed_result("Finance officer", f"{finance_officer.username}/password123", created)

    # Accredited Investor (verified, can pledge large amounts)
    accredited_investor, created = User.objects.update_or_create(
        username='accredited_investor',
        defaults={
            'email': 'accredited@example.com',
            'role': User.Role.INVESTOR,
            'first_name': 'Sarah',
            'last_name': 'Capital',
            'is_staff': False,
            'is_superuser': False,
        },
    )
    accredited_investor.set_password('password123')
    accredited_investor.save(update_fields=['password'])
    log_seed_result("Accredited investor", f"{accredited_investor.username}/password123", created)

    # Buyer with credit needs
    credit_buyer, created = User.objects.update_or_create(
        username='credit_buyer',
        defaults={
            'email': 'buyer.credit@example.com',
            'role': User.Role.PROJECT_OWNER,
            'first_name': 'Michael',
            'last_name': 'Buyer',
            'is_staff': False,
            'is_superuser': False,
        },
    )
    credit_buyer.set_password('password123')
    credit_buyer.save(update_fields=['password'])
    log_seed_result("Credit buyer", f"{credit_buyer.username}/password123", created)

    # Verified vendor with credit line
    credit_vendor, created = User.objects.update_or_create(
        username='credit_vendor',
        defaults={
            'email': 'vendor.credit@example.com',
            'role': User.Role.VENDOR,
            'first_name': 'Grace',
            'last_name': 'Supplier',
            'is_staff': False,
            'is_superuser': False,
        },
    )
    credit_vendor.set_password('password123')
    credit_vendor.save(update_fields=['password'])
    log_seed_result("Credit vendor", f"{credit_vendor.username}/password123", created)

    # Contractor with working capital needs
    credit_contractor, created = User.objects.update_or_create(
        username='credit_contractor',
        defaults={
            'email': 'contractor.credit@example.com',
            'role': User.Role.CONTRACTOR,
            'first_name': 'James',
            'last_name': 'Builder',
            'is_staff': False,
            'is_superuser': False,
        },
    )
    credit_contractor.set_password('password123')
    credit_contractor.save(update_fields=['password'])
    log_seed_result("Credit contractor", f"{credit_contractor.username}/password123", created)

    return (
        finance_officer,
        accredited_investor,
        credit_buyer,
        credit_vendor,
        credit_contractor,
    )


def seed_finance_products():
    """Create standard finance products available on the platform."""
    products = [
        {
            'name': 'Material Procurement Credit',
            'provider_name': 'Procus Capital',
            'max_amount': 5000000.00,
            'interest_rate': 9.50,
        },
        {
            'name': 'Contractor Working Capital',
            'provider_name': 'BuildBank Kenya',
            'max_amount': 10000000.00,
            'interest_rate': 12.00,
        },
        {
            'name': 'Project Completion Loan',
            'provider_name': 'InfraFinance',
            'max_amount': 25000000.00,
            'interest_rate': 11.25,
        },
        {
            'name': 'Property Acquisition Facility',
            'provider_name': 'Procus Capital',
            'max_amount': 50000000.00,
            'interest_rate': 10.75,
        },
        {
            'name': 'Vendor Inventory Credit',
            'provider_name': 'SupplyLine Finance',
            'max_amount': 3000000.00,
            'interest_rate': 8.50,
        },
        {
            'name': 'Renovation Bridge Loan',
            'provider_name': 'BuildBank Kenya',
            'max_amount': 15000000.00,
            'interest_rate': 13.50,
        },
    ]

    created_products = {}
    for spec in products:
        product, created = FinanceProduct.objects.update_or_create(
            name=spec['name'],
            defaults={**spec, 'active': True},
        )
        created_products[spec['name']] = product
        log_seed_result("Finance product", product.name, created)

    return created_products


def seed_finance_applications(products, credit_buyer, credit_contractor, credit_vendor):
    """Create finance applications in various statuses."""
    apps = []

    # Buyer applies for material credit
    app1, created = FinanceApplication.objects.update_or_create(
        applicant=credit_buyer,
        product=products['Material Procurement Credit'],
        target_type=FinanceApplication.TargetType.MATERIAL_ORDER,
        defaults={
            'requested_amount': 850000.00,
            'purpose_category': FinanceApplication.PurposeCategory.MATERIALS_PROCUREMENT,
            'purpose': 'Procure cement, steel reinforcement, and timber framing for residential extension.',
            'status': FinanceApplication.Status.APPROVED,
        },
    )
    log_seed_result("Finance application", f"{app1.applicant.username} / {app1.product.name} / {app1.status}", created)
    apps.append(app1)

    # Contractor applies for working capital
    app2, created = FinanceApplication.objects.update_or_create(
        applicant=credit_contractor,
        product=products['Contractor Working Capital'],
        target_type=FinanceApplication.TargetType.CONTRACT,
        defaults={
            'requested_amount': 3200000.00,
            'purpose_category': FinanceApplication.PurposeCategory.WORKING_CAPITAL,
            'purpose': 'Bridge payroll and equipment rental between milestone payments.',
            'status': FinanceApplication.Status.SUBMITTED,
        },
    )
    log_seed_result("Finance application", f"{app2.applicant.username} / {app2.product.name} / {app2.status}", created)
    apps.append(app2)

    # Vendor applies for inventory credit
    app3, created = FinanceApplication.objects.update_or_create(
        applicant=credit_vendor,
        product=products['Vendor Inventory Credit'],
        target_type=FinanceApplication.TargetType.GENERAL_WORKING_CAPITAL,
        defaults={
            'requested_amount': 1500000.00,
            'purpose_category': FinanceApplication.PurposeCategory.WORKING_CAPITAL,
            'purpose': 'Stock bulk cement and steel bars ahead of Q3 demand surge.',
            'status': FinanceApplication.Status.DISBURSED,
        },
    )
    log_seed_result("Finance application", f"{app3.applicant.username} / {app3.product.name} / {app3.status}", created)
    apps.append(app3)

    # Another buyer applies for renovation loan
    app4, created = FinanceApplication.objects.update_or_create(
        applicant=credit_buyer,
        product=products['Renovation Bridge Loan'],
        target_type=FinanceApplication.TargetType.PROPERTY,
        defaults={
            'requested_amount': 4200000.00,
            'purpose_category': FinanceApplication.PurposeCategory.RENOVATION,
            'purpose': 'Complete kitchen and bathroom renovation before tenancy commencement.',
            'status': FinanceApplication.Status.REJECTED,
        },
    )
    log_seed_result("Finance application", f"{app4.applicant.username} / {app4.product.name} / {app4.status}", created)
    apps.append(app4)

    return apps


def seed_finance_loans(apps):
    """Create loans for approved/disbursed applications."""
    loans = []
    for app in apps:
        if app.status not in (FinanceApplication.Status.APPROVED, FinanceApplication.Status.DISBURSED):
            continue

        loan, created = FinanceLoan.objects.update_or_create(
            application=app,
            defaults={
                'principal_amount': app.requested_amount,
                'disbursed_amount': app.requested_amount if app.status == FinanceApplication.Status.DISBURSED else app.requested_amount * 0.5,
                'repayment_due_date': timezone.now().date() + timedelta(days=180),
                'status': FinanceLoan.Status.ACTIVE,
            },
        )
        log_seed_result(
            "Finance loan",
            f"{loan.application.applicant.username} / KES {loan.principal_amount:,.2f} / {loan.status}",
            created,
        )
        loans.append(loan)
    return loans


def seed_finance_repayments(loans):
    """Create sample repayments for active loans."""
    for loan in loans:
        # First repayment
        rep1, created = FinanceRepayment.objects.update_or_create(
            loan=loan,
            payment_reference=f"REP-{loan.id}-001",
            defaults={
                'amount': loan.principal_amount * 0.25,
                'paid_at': timezone.now() - timedelta(days=30),
            },
        )
        log_seed_result("Finance repayment", rep1.payment_reference, created)

        # Second repayment (for disbursed loans)
        if loan.application.status == FinanceApplication.Status.DISBURSED:
            rep2, created = FinanceRepayment.objects.update_or_create(
                loan=loan,
                payment_reference=f"REP-{loan.id}-002",
                defaults={
                    'amount': loan.principal_amount * 0.25,
                    'paid_at': timezone.now() - timedelta(days=5),
                },
            )
            log_seed_result("Finance repayment", rep2.payment_reference, created)


def seed_supplier_credit_lines(credit_vendor):
    """Create a supplier credit line for the demo vendor."""
    credit_line, created = SupplierCreditLine.objects.update_or_create(
        vendor=credit_vendor.vendor_profile if hasattr(credit_vendor, 'vendor_profile') else None,
        defaults={
            'credit_limit': 2000000.00,
            'available_balance': 850000.00,
            'status': SupplierCreditLine.Status.ACTIVE,
        },
    )
    log_seed_result(
        "Supplier credit line",
        f"{credit_vendor.username} / KES {credit_line.credit_limit:,.2f}",
        created,
    )


def seed_investor_profiles(accredited_investor):
    """Create verified investor profile."""
    profile, created = InvestorProfile.objects.update_or_create(
        user=accredited_investor,
        defaults={
            'kyc_status': InvestorProfile.KYCStatus.VERIFIED,
            'accreditation_status': InvestorProfile.AccreditationStatus.ACCREDITED,
            'jurisdiction': 'Kenya',
        },
    )
    log_seed_result("Investor profile", f"{profile.user.username} / {profile.kyc_status}", created)
    return profile


def seed_investment_agreements(accredited_investor):
    """Create sample investment agreements."""
    from projects.models import Project

    # Find or create a fundable project
    project, created = Project.objects.update_or_create(
        title='Kilimani Residential Tower',
        defaults={
            'owner': accredited_investor,
            'description': '12-storey residential tower with 48 units and rooftop amenities.',
            'location_text': 'Kilimani, Nairobi',
            'estimated_budget': 45000000.00,
            'funding_required': True,
            'status': 'FUNDING_OPEN',
        },
    )
    log_seed_result("Seed project", project.title, created)

    # Draft agreement
    agr1, created = InvestmentAgreement.objects.update_or_create(
        project=project,
        investor=accredited_investor,
        defaults={
            'amount': 5000000.00,
            'agreement_terms_url': 'https://example.com/terms/sample-agreement.pdf',
            'status': InvestmentAgreement.Status.DRAFT,
            'signed_at': None,
        },
    )
    log_seed_result("Investment agreement", f"{agr1.project.title} / {agr1.status}", created)

    # Signed agreement
    agr2, created = InvestmentAgreement.objects.update_or_create(
        project=project,
        investor=accredited_investor,
        amount=7500000.00,
        defaults={
            'agreement_terms_url': 'https://example.com/terms/signed-agreement.pdf',
            'status': InvestmentAgreement.Status.SIGNED,
            'signed_at': timezone.now() - timedelta(days=14),
        },
    )
    log_seed_result("Investment agreement", f"{agr2.project.title} / {agr2.status}", created)

    return [agr1, agr2]


def seed_bank_accounts(finance_officer, accredited_investor, credit_contractor):
    """Create bank accounts for payouts and settlements."""
    accounts = [
        {
            'user': finance_officer,
            'bank_name': 'Equity Bank',
            'account_number_last4': '8877',
            'routing_number': 'EQBLKENA',
            'currency': 'KES',
        },
        {
            'user': accredited_investor,
            'bank_name': 'KCB Bank',
            'account_number_last4': '5544',
            'routing_number': 'KCBLKENX',
            'currency': 'KES',
        },
        {
            'user': credit_contractor,
            'bank_name': 'Co-operative Bank',
            'account_number_last4': '3322',
            'routing_number': 'COOPKENA',
            'currency': 'KES',
        },
    ]

    created_accounts = []
    for spec in accounts:
        account, created = BankAccount.objects.update_or_create(
            user=spec['user'],
            bank_name=spec['bank_name'],
            account_number_last4=spec['account_number_last4'],
            defaults={
                'routing_number': spec['routing_number'],
                'currency': spec['currency'],
                'is_verified': True,
                'external_id': f"ext_{spec['user'].username}_{spec['account_number_last4']}",
            },
        )
        created_accounts.append(account)
        log_seed_result("Bank account", f"{account.user.username} / {account.bank_name} ****{account.account_number_last4}", created)

    return created_accounts


def seed_settlement_transactions(accounts):
    """Create sample settlement transactions."""
    for account in accounts:
        st, created = SettlementTransaction.objects.update_or_create(
            destination_account=account,
            reference=f"SETTLE-{account.user.username.upper()}-001",
            defaults={
                'amount': 125000.00,
                'status': SettlementTransaction.Status.PROCESSED,
            },
        )
        log_seed_result("Settlement", st.reference, created)


def seed_escrow_samples(accredited_investor, credit_contractor):
    """Create sample escrow account and transaction."""
    from contracts.models import Contract

    contract, created = Contract.objects.update_or_create(
        title='Foundation & Structural Works',
        defaults={
            'owner': accredited_investor,
            'description_scope': 'Complete foundation and structural framework for residential tower.',
            'location': 'Kilimani, Nairobi',
            'budget_min': 8000000.00,
            'budget_max': 12000000.00,
            'currency': 'KES',
            'status': 'AWARDED',
        },
    )
    log_seed_result("Seed contract", contract.title, created)

    escrow, created = EscrowAccount.objects.update_or_create(
        contract=contract,
        defaults={
            'buyer': accredited_investor,
            'total_amount_held': 5000000.00,
            'currency': 'KES',
            'status': EscrowAccount.Status.ACTIVE,
        },
    )
    log_seed_result("Escrow account", f"Escrow #{escrow.id} / {contract.title}", created)

    # Deposit transaction
    tx, created = EscrowTransaction.objects.update_or_create(
        escrow_account=escrow,
        payment_reference=f"DEP-{escrow.id}",
        defaults={
            'type': EscrowTransaction.Type.DEPOSIT,
            'amount': 5000000.00,
        },
    )
    log_seed_result("Escrow transaction", tx.payment_reference, created)


def run():
    log_seed_banner("💰 Starting Finance Workflow Seed")

    (
        finance_officer,
        accredited_investor,
        credit_buyer,
        credit_vendor,
        credit_contractor,
    ) = ensure_finance_users()

    products = seed_finance_products()
    apps = seed_finance_applications(products, credit_buyer, credit_contractor, credit_vendor)
    loans = seed_finance_loans(apps)
    seed_finance_repayments(loans)

    # Ensure vendor profile exists for credit_vendor, then seed supplier credit
    from vendors.models import Vendor
    vendor_profile, created = Vendor.objects.update_or_create(
        user=credit_vendor,
        defaults={
            'business_name': 'Grace Supplies Ltd',
            'registration_number': 'GRS-2026-001',
            'verified_status': Vendor.Status.APPROVED,
            'location_text': 'Industrial Area, Nairobi',
        },
    )
    log_seed_result("Vendor profile", vendor_profile.business_name, created)
    seed_supplier_credit_lines(credit_vendor)

    seed_investor_profiles(accredited_investor)
    seed_investment_agreements(accredited_investor)
    accounts = seed_bank_accounts(finance_officer, accredited_investor, credit_contractor)
    seed_settlement_transactions(accounts)
    seed_escrow_samples(accredited_investor, credit_contractor)

    log_seed_banner("✅ Finance Workflow Seed Complete")
    logger.info("")
    logger.info("📋 Demo Credentials:")
    logger.info("  finance_officer / password123")
    logger.info("  accredited_investor / password123")
    logger.info("  credit_buyer / password123")
    logger.info("  credit_vendor / password123")
    logger.info("  credit_contractor / password123")


if __name__ == '__main__':
    run()
