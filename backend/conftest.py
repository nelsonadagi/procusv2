import pytest
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
import factory
from accounts.models import Organization
from contracts.models import Contract
from escrow.models import EscrowAccount
from milestones.models import Milestone

User = get_user_model()

class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization
    
    name = factory.Faker('company')
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(' ', '-'))

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = User.Role.PROJECT_OWNER

class ContractFactory(DjangoModelFactory):
    class Meta:
        model = Contract
    
    owner = factory.SubFactory(UserFactory, role=User.Role.PROJECT_OWNER)
    title = factory.Faker('sentence')
    description_scope = factory.Faker('paragraph')
    location = factory.Faker('city')
    budget_min = 1000
    budget_max = 5000
    status = 'POSTED'

class EscrowAccountFactory(DjangoModelFactory):
    class Meta:
        model = EscrowAccount
    
    contract = factory.SubFactory(ContractFactory)
    buyer = factory.SelfAttribute('contract.owner')
    total_amount_held = 0
    status = EscrowAccount.Status.ACTIVE

class MilestoneFactory(DjangoModelFactory):
    class Meta:
        model = Milestone
    
    contract = factory.SubFactory(ContractFactory)
    title = factory.Faker('sentence')
    amount = 500
    due_date = factory.Faker('date_this_year')
    status = 'PENDING'

@pytest.fixture
def user_factory():
    return UserFactory

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def project_owner(db):
    return UserFactory(role=User.Role.PROJECT_OWNER)

@pytest.fixture
def contractor(db):
    return UserFactory(role=User.Role.CONTRACTOR)

@pytest.fixture
def vendor(db):
    return UserFactory(role=User.Role.VENDOR)

@pytest.fixture
def admin_user(db):
    return UserFactory(role=User.Role.ADMIN, is_staff=True, is_superuser=True)
