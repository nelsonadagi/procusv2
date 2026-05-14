#!/usr/bin/env python3
"""
API-only Python HTTP harness that exercises the marketplace like a frontend client.

It logs in as seeded actors, performs a small set of write workflows for the
most important modules, and then sweeps the rest of the mounted API surface
with authenticated GET requests.

Default target:
    http://localhost:8007

Examples:
    python backend/scripts/e2e_frontend_runner.py
    python backend/scripts/e2e_frontend_runner.py --mode smoke
    python backend/scripts/e2e_frontend_runner.py --module projects --module property
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence

import requests


DEFAULT_TIMEOUT = 25.0
DEFAULT_BASE_URL = "http://localhost:8007"
DEFAULT_COUNTRY = "KE"
DEFAULT_STARTUP_WAIT = 180.0
DEFAULT_RETRY_DELAY = 2.0


@dataclass(frozen=True)
class Actor:
    key: str
    login: str
    password: str


ACTORS: Dict[str, Actor] = {
    "admin": Actor("admin", "admin", "adminpassword123"),
    "owner": Actor("owner", "owner_jane", "Starten1@"),
    "vendor": Actor("vendor", "vendor_mall", "Starten1@"),
    "contractor": Actor("contractor", "contractor_expert", "Starten1@"),
    "investor": Actor("investor", "investor_wealth", "Starten1@"),
    "property_manager": Actor("property_manager", "property_ops", "Starten1@"),
    "government": Actor("government", "gov_authority", "Starten1@"),
    "courier": Actor("courier", "courier_fast", "Starten1@"),
}


@dataclass
class Client:
    actor: Actor
    base_url: str
    timeout: float
    country: str
    session: requests.Session = field(default_factory=requests.Session)
    token: Optional[str] = None
    user: Dict[str, Any] = field(default_factory=dict)
    startup_wait: float = DEFAULT_STARTUP_WAIT
    retry_delay: float = DEFAULT_RETRY_DELAY

    def wait_until_ready(self) -> None:
        deadline = time.time() + self.startup_wait
        last_error = "backend not yet reachable"

        while time.time() < deadline:
            try:
                response = self.session.get(
                    f"{self.base_url}/api/platform_settings/platform/",
                    headers={"X-Active-Country": self.country},
                    timeout=min(self.timeout, 10.0),
                )
                if response.status_code < HTTPStatus.INTERNAL_SERVER_ERROR:
                    return
                last_error = f"readiness endpoint returned {response.status_code}"
            except requests.RequestException as exc:
                last_error = str(exc)
            time.sleep(self.retry_delay)

        raise RuntimeError(
            f"API not ready after {int(self.startup_wait)}s at {self.base_url}: {last_error}"
        )

    def login(self) -> None:
        self.wait_until_ready()
        response = self.raw_request(
            "POST",
            "/api/accounts/login/",
            json_body={"email": self.actor.login, "password": self.actor.password},
            headers={"X-Active-Country": self.country},
            expected=(200,),
        )
        response.raise_for_status()
        payload = response.json()
        self.token = payload["token"]
        self.user = payload.get("user", {})
        self.session.headers.update(
            {
                "Authorization": f"Token {self.token}",
                "X-Active-Country": self.country,
            }
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        expected: Sequence[int] = (200,),
    ) -> requests.Response:
        response = self.raw_request(
            method,
            path,
            json_body=json_body,
            params=params,
            expected=expected,
        )
        if response.status_code not in expected:
            raise AssertionError(
                f"{method.upper()} {path} returned {response.status_code}, expected {sorted(set(expected))}: "
                f"{truncate(response.text)}"
            )
        return response

    def raw_request(
        self,
        method: str,
        path: str,
        *,
        json_body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        expected: Sequence[int] = (200,),
    ) -> requests.Response:
        deadline = time.time() + self.startup_wait
        last_error: Optional[Exception] = None

        while True:
            try:
                response = self.session.request(
                    method=method.upper(),
                    url=f"{self.base_url}{path}",
                    json=json_body,
                    params=params,
                    headers=headers,
                    timeout=self.timeout,
                )
                if response.status_code == HTTPStatus.TOO_MANY_REQUESTS and time.time() < deadline:
                    retry_after = response.headers.get("Retry-After")
                    try:
                        wait_seconds = max(float(retry_after), self.retry_delay) if retry_after else self.retry_delay
                    except ValueError:
                        wait_seconds = self.retry_delay
                    print(
                        f"[WAIT] {method.upper()} {path} throttled for {int(wait_seconds)}s; retrying..."
                    )
                    time.sleep(wait_seconds)
                    continue
                if response.status_code < HTTPStatus.INTERNAL_SERVER_ERROR:
                    return response
                if time.time() >= deadline:
                    return response
                last_error = RuntimeError(
                    f"{method.upper()} {path} returned transient {response.status_code}"
                )
            except requests.RequestException as exc:
                if time.time() >= deadline:
                    raise exc
                last_error = exc

            time.sleep(self.retry_delay)

            if expected and isinstance(last_error, RuntimeError):
                continue


@dataclass
class StepResult:
    name: str
    module: str
    actor: str
    status: str
    http_status: Optional[int]
    duration_ms: int
    detail: str


def truncate(value: Any, limit: int = 220) -> str:
    text = value if isinstance(value, str) else json.dumps(value, default=str)
    if len(text) <= limit:
        return text
    return f"{text[: limit - 3]}..."


def read_json(response: requests.Response) -> Any:
    if not response.text.strip():
        return {}
    try:
        return response.json()
    except ValueError:
        return {"raw": response.text}


def list_items(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        return payload["results"]
    if isinstance(payload, list):
        return payload
    return []


def first_identifier(payload: Any, keys: Iterable[str] = ("id", "uuid")) -> Optional[Any]:
    items = list_items(payload)
    if not items:
        return None
    first = items[0]
    for key in keys:
        if key in first and first[key] not in (None, ""):
            return first[key]
    return None


def collect_identifiers(payload: Any, keys: Iterable[str] = ("id", "uuid")) -> List[str]:
    identifiers: List[str] = []
    for item in list_items(payload):
        for key in keys:
            value = item.get(key)
            if value not in (None, ""):
                identifiers.append(str(value))
                break
    return identifiers


def find_country_id(payload: Any, iso_code: str) -> Optional[Any]:
    target = iso_code.upper()
    for item in list_items(payload):
        if str(item.get("iso_code", "")).upper() == target:
            return item.get("id")
    return None


def build_authenticated_client(
    template_client: Client,
    *,
    actor_key: str,
    login: str,
    password: str,
    token: Optional[str] = None,
    user: Optional[Dict[str, Any]] = None,
) -> Client:
    client = Client(
        actor=Actor(actor_key, login, password),
        base_url=template_client.base_url,
        timeout=template_client.timeout,
        country=template_client.country,
        startup_wait=template_client.startup_wait,
        retry_delay=template_client.retry_delay,
    )
    if token:
        client.token = token
        client.user = user or {}
        client.session.headers.update(
            {
                "Authorization": f"Token {token}",
                "X-Active-Country": template_client.country,
            }
        )
        return client
    client.login()
    return client


def resolve_country_id(client: Client) -> Any:
    countries = read_json(client.request("GET", "/api/platform_settings/countries/", expected=(200,)))
    country_id = find_country_id(countries, client.country)
    if not country_id:
        raise AssertionError(f"Could not resolve active country id for {client.country}")
    return country_id


def register_account(
    template_client: Client,
    state: Dict[str, Any],
    *,
    account_key: str,
    first_name: str,
    last_name: str,
) -> Dict[str, Any]:
    username = make_unique(account_key, state)
    email = f"{username}@example.com"
    password = f"Starten1@{state['run_id']}"
    session = requests.Session()
    deadline = time.time() + template_client.startup_wait
    while True:
        response = session.post(
            f"{template_client.base_url}/api/accounts/register/",
            json={
                "username": username,
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
            },
            headers={"X-Active-Country": template_client.country},
            timeout=template_client.timeout,
        )
        if response.status_code == HTTPStatus.CREATED:
            break
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS and time.time() < deadline:
            retry_after = response.headers.get("Retry-After")
            try:
                wait_seconds = max(float(retry_after), template_client.retry_delay) if retry_after else template_client.retry_delay
            except ValueError:
                wait_seconds = template_client.retry_delay
            print(
                f"[WAIT] POST /api/accounts/register/ throttled for {int(wait_seconds)}s; retrying..."
            )
            time.sleep(wait_seconds)
            continue
        raise AssertionError(
            f"POST /api/accounts/register/ returned {response.status_code}: {truncate(response.text)}"
        )
    payload = read_json(response)
    account_client = build_authenticated_client(
        template_client,
        actor_key=account_key,
        login=username,
        password=password,
        token=payload.get("token"),
        user=payload.get("user", {}),
    )
    return {
        "username": username,
        "email": email,
        "password": password,
        "user": payload.get("user", {}),
        "client": account_client,
    }


def admin_find_user(admin_client: Client, email: str) -> Dict[str, Any]:
    users = read_json(admin_client.request("GET", "/api/platform_settings/admin-users/", expected=(200,)))
    for user in users:
        if str(user.get("email", "")).lower() == email.lower():
            return user
    raise AssertionError(f"Admin user list did not include {email}")


def admin_set_role(admin_client: Client, user_id: Any, role: str) -> Dict[str, Any]:
    return read_json(
        admin_client.request(
            "PATCH",
            f"/api/platform_settings/admin-users/{user_id}/set_role/",
            json_body={"role": role},
            expected=(200,),
        )
    )


def find_item(payload: Any, predicate: Callable[[Dict[str, Any]], bool]) -> Optional[Dict[str, Any]]:
    for item in list_items(payload):
        if predicate(item):
            return item
    return None


class Harness:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.clients: Dict[str, Client] = {}
        self.results: List[StepResult] = []
        self.state: Dict[str, Any] = {"run_id": uuid.uuid4().hex[:8]}

    def client(self, actor_key: str) -> Client:
        if actor_key not in self.clients:
            actor = ACTORS[actor_key]
            client = Client(
                actor=actor,
                base_url=self.args.base_url.rstrip("/"),
                timeout=self.args.timeout,
                country=self.args.country,
                startup_wait=self.args.startup_wait,
                retry_delay=self.args.retry_delay,
            )
            client.login()
            self.clients[actor_key] = client
        return self.clients[actor_key]

    def selected(self, module: str) -> bool:
        return not self.args.module or module in self.args.module

    def run_step(
        self,
        *,
        module: str,
        name: str,
        actor: str,
        func: Callable[[Client, Dict[str, Any]], str],
    ) -> None:
        if not self.selected(module):
            return

        started = time.perf_counter()
        http_status = None
        detail = ""
        status = "PASS"
        try:
            detail = func(self.client(actor), self.state)
        except Exception as exc:  # pragma: no cover - intentional harness behavior
            status = "FAIL"
            detail = str(exc)
            if isinstance(exc, requests.HTTPError) and exc.response is not None:
                http_status = exc.response.status_code
            elif isinstance(exc, AssertionError):
                status_code = extract_status_code(str(exc))
                if status_code is not None:
                    http_status = status_code
        duration_ms = int((time.perf_counter() - started) * 1000)
        self.results.append(
            StepResult(
                name=name,
                module=module,
                actor=actor,
                status=status,
                http_status=http_status,
                duration_ms=duration_ms,
                detail=truncate(detail),
            )
        )
        label = f"[{status}] {module}:{name} ({actor}) {duration_ms}ms"
        if status == "PASS":
            print(f"{label} :: {detail}")
        else:
            print(f"{label} :: {detail}", file=sys.stderr)
            if self.args.fail_fast:
                raise SystemExit(1)

    def summary(self) -> int:
        passed = sum(1 for item in self.results if item.status == "PASS")
        failed = len(self.results) - passed
        print("\n=== Summary ===")
        print(f"Total steps: {len(self.results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        return 1 if failed else 0


def extract_status_code(message: str) -> Optional[int]:
    tokens = message.split()
    for token in tokens:
        if token.isdigit() and len(token) == 3:
            try:
                return int(token)
            except ValueError:
                return None
    return None


def make_unique(prefix: str, state: Dict[str, Any]) -> str:
    return f"{prefix}-{state['run_id']}"


def public_bootstrap(client: Client, state: Dict[str, Any]) -> str:
    del state
    endpoints = [
        ("/api/platform_settings/platform/", None),
        ("/api/platform_settings/countries/", None),
        ("/api/platform_settings/currencies/", None),
        ("/api/taxonomy/categories/", {"taxonomy_type": "MATERIAL"}),
        ("/api/v1/products/locations/", {"country": client.country}),
        ("/api/v1/products/", {"page": 1, "page_size": 12, "country": client.country}),
    ]
    for path, params in endpoints:
        client.request("GET", path, params=params, expected=(200,))
    return "platform bootstrap endpoints responded"


def owner_self_registration(client: Client, state: Dict[str, Any]) -> str:
    account = register_account(
        client,
        state,
        account_key="owner-onboard",
        first_name="Owner",
        last_name="Applicant",
    )
    owner_client = account["client"]
    if account["user"].get("role") != "PROJECT_OWNER":
        raise AssertionError(
            f"Fresh registration should default to PROJECT_OWNER, got {account['user'].get('role')}"
        )
    owner_client.request(
        "PATCH",
        "/api/accounts/profile/",
        json_body={
            "first_name": "Onboarded",
            "profile": {
                "preferred_region": "Nairobi",
                "delivery_instructions": "Call on arrival",
            },
        },
        expected=(200,),
    )
    address = read_json(
        owner_client.request(
            "POST",
            "/api/accounts/addresses/",
            json_body={
                "name": f"Owner HQ {state['run_id']}",
                "address_line_1": "123 Builder Avenue",
                "city": "Nairobi",
                "state_province": "Nairobi",
                "postal_code": "00100",
                "country": "Kenya",
                "is_default": True,
            },
            expected=(201,),
        )
    )
    return f"registered owner account={account['email']} address_id={address.get('id')}"


def vendor_admin_approval_onboarding(client: Client, state: Dict[str, Any]) -> str:
    account = register_account(
        client,
        state,
        account_key="vendor-onboard",
        first_name="Vendor",
        last_name="Applicant",
    )
    admin_user = admin_find_user(client, account["email"])
    role_update = admin_set_role(client, admin_user["id"], "VENDOR")
    if role_update.get("role") != "VENDOR":
        raise AssertionError(f"Admin failed to set vendor role: {truncate(role_update)}")

    vendor_client = account["client"]
    missing_profile = vendor_client.raw_request("GET", "/api/vendors/me/", expected=(403,))
    if missing_profile.status_code != 403:
        raise AssertionError(
            f"Expected /api/vendors/me/ to return 403 before onboarding, got {missing_profile.status_code}"
        )

    created = read_json(
        vendor_client.request(
            "POST",
            "/api/vendors/",
            json_body={
                "business_name": make_unique("Vendor Works", state),
                "registration_number": make_unique("VREG", state),
                "country": resolve_country_id(vendor_client),
                "location": "Nairobi",
                "provides_delivery": True,
                "delivery_radius_km": 20,
                "categories_served": ["Cement", "Steel"],
            },
            expected=(201,),
        )
    )
    vendor_id = created.get("id")
    pending_profile = read_json(vendor_client.request("GET", "/api/vendors/me/", expected=(200,)))
    if pending_profile.get("verified_status") != "PENDING":
        raise AssertionError(
            f"Vendor onboarding should start as PENDING: {truncate(pending_profile)}"
        )

    approved = read_json(
        client.request("POST", f"/api/vendors/{vendor_id}/approve/", expected=(200,))
    )
    if approved.get("verified_status") != "APPROVED":
        raise AssertionError(f"Vendor approval did not reach APPROVED: {truncate(approved)}")

    me_payload = read_json(vendor_client.request("GET", "/api/vendors/me/", expected=(200,)))
    if me_payload.get("verified_status") != "APPROVED":
        raise AssertionError(f"Vendor profile did not reflect approval: {truncate(me_payload)}")
    return f"vendor account approved email={account['email']} vendor_id={vendor_id}"


def contractor_admin_approval_onboarding(client: Client, state: Dict[str, Any]) -> str:
    account = register_account(
        client,
        state,
        account_key="contractor-onboard",
        first_name="Contractor",
        last_name="Applicant",
    )
    admin_user = admin_find_user(client, account["email"])
    role_update = admin_set_role(client, admin_user["id"], "CONTRACTOR")
    if role_update.get("role") != "CONTRACTOR":
        raise AssertionError(f"Admin failed to set contractor role: {truncate(role_update)}")

    contractor_client = account["client"]
    missing_profile = contractor_client.raw_request("GET", "/api/v2/contractors/me/", expected=(404,))
    if missing_profile.status_code != 404:
        raise AssertionError(
            f"Expected /api/v2/contractors/me/ to return 404 before onboarding, got {missing_profile.status_code}"
        )

    created = read_json(
        contractor_client.request(
            "POST",
            "/api/v2/contractors/register/",
            json_body={
                "company_name": make_unique("Contractor Works", state),
                "service_categories": ["General Construction"],
                "country": resolve_country_id(contractor_client),
                "location_text": "Nairobi",
                "service_radius_km": 25,
            },
            expected=(201,),
        )
    )
    contractor_id = created.get("id")
    if created.get("verified_status") != "PENDING":
        raise AssertionError(f"Contractor onboarding should start as PENDING: {truncate(created)}")

    approved = read_json(
        client.request("POST", f"/api/v2/contractors/{contractor_id}/approve/", expected=(200,))
    )
    if approved.get("verified_status") != "APPROVED":
        raise AssertionError(f"Contractor approval did not reach APPROVED: {truncate(approved)}")

    me_payload = read_json(
        contractor_client.request("GET", "/api/v2/contractors/me/", expected=(200,))
    )
    if me_payload.get("verified_status") != "APPROVED":
        raise AssertionError(f"Contractor profile did not reflect approval: {truncate(me_payload)}")
    return f"contractor account approved email={account['email']} contractor_id={contractor_id}"


def investor_admin_approval_onboarding(client: Client, state: Dict[str, Any]) -> str:
    account = register_account(
        client,
        state,
        account_key="investor-onboard",
        first_name="Investor",
        last_name="Applicant",
    )
    admin_user = admin_find_user(client, account["email"])
    role_update = admin_set_role(client, admin_user["id"], "INVESTOR")
    if role_update.get("role") != "INVESTOR":
        raise AssertionError(f"Admin failed to set investor role: {truncate(role_update)}")

    investor_client = account["client"]
    profile = read_json(
        investor_client.request(
            "POST",
            "/api/v5/investors/onboard/",
            json_body={"jurisdiction": "Kenya"},
            expected=(201,),
        )
    )
    kyc = read_json(
        investor_client.request(
            "POST",
            "/api/compliance/kyc-verifications/",
            json_body={
                "document_type": "National ID",
                "document_number": make_unique("INVESTOR-ID", state),
                "document_url": "https://example.com/docs/investor-id.pdf",
            },
            expected=(201,),
        )
    )
    if kyc.get("status") != "SUBMITTED":
        raise AssertionError(f"Investor KYC should start as SUBMITTED: {truncate(kyc)}")

    kyc_records = read_json(client.request("GET", "/api/compliance/kyc-verifications/", expected=(200,)))
    kyc_record = find_item(
        kyc_records,
        lambda item: str(item.get("user_email", "")).lower() == account["email"].lower(),
    )
    if not kyc_record:
        raise AssertionError(f"Admin KYC queue did not include {account['email']}")

    approved = read_json(
        client.request(
            "POST",
            f"/api/compliance/kyc-verifications/{kyc_record['id']}/approve/",
            expected=(200,),
        )
    )
    if approved.get("status") != "VERIFIED":
        raise AssertionError(f"KYC approval did not reach VERIFIED: {truncate(approved)}")

    own_records = read_json(
        investor_client.request("GET", "/api/compliance/kyc-verifications/", expected=(200,))
    )
    own_record = find_item(
        own_records,
        lambda item: item.get("document_number") == kyc.get("document_number"),
    )
    if not own_record or own_record.get("status") != "VERIFIED":
        raise AssertionError(f"Investor cannot see VERIFIED KYC record: {truncate(own_records)}")
    return f"investor account approved email={account['email']} profile_id={profile.get('id')} kyc_id={kyc_record['id']}"


def courier_admin_approval_onboarding(client: Client, state: Dict[str, Any]) -> str:
    account = register_account(
        client,
        state,
        account_key="courier-onboard",
        first_name="Courier",
        last_name="Applicant",
    )
    admin_user = admin_find_user(client, account["email"])
    role_update = admin_set_role(client, admin_user["id"], "COURIER")
    if role_update.get("role") != "COURIER":
        raise AssertionError(f"Admin failed to set courier role: {truncate(role_update)}")

    courier_client = account["client"]
    missing_profile = courier_client.raw_request("GET", "/api/logistics/couriers/me/", expected=(404,))
    if missing_profile.status_code != 404:
        raise AssertionError(
            f"Expected /api/logistics/couriers/me/ to return 404 before onboarding, got {missing_profile.status_code}"
        )

    created = read_json(
        courier_client.request(
            "POST",
            "/api/logistics/couriers/",
            json_body={
                "company_name": make_unique("Courier Works", state),
                "registration_number": make_unique("CREG", state),
                "tax_pin": make_unique("PIN", state),
                "support_email": account["email"],
                "support_phone": "+254700000001",
                "country": resolve_country_id(courier_client),
                "location": "Nairobi",
            },
            expected=(201,),
        )
    )
    me_payload = read_json(
        courier_client.request("GET", "/api/logistics/couriers/me/", expected=(200,))
    )
    return (
        f"courier account role-approved email={account['email']} courier_id={created.get('id')} "
        f"status={me_payload.get('status', 'unknown')}"
    )


def government_admin_approval_onboarding(client: Client, state: Dict[str, Any]) -> str:
    account = register_account(
        client,
        state,
        account_key="government-onboard",
        first_name="Government",
        last_name="Officer",
    )
    admin_user = admin_find_user(client, account["email"])
    role_update = admin_set_role(client, admin_user["id"], "GOVERNMENT")
    if role_update.get("role") != "GOVERNMENT":
        raise AssertionError(f"Admin failed to set government role: {truncate(role_update)}")

    government_client = account["client"]
    tender = read_json(
        government_client.request(
            "POST",
            "/api/v5/tenders/",
            json_body={
                "title": make_unique("Public Tender", state),
                "description": "Government onboarding tender publication check",
                "issuing_authority": "Ministry of Public Works",
                "bid_deadline": "2030-01-01T09:00:00Z",
            },
            expected=(201,),
        )
    )
    return f"government account role-approved email={account['email']} tender_id={tender.get('id')}"


def profile_and_address(client: Client, state: Dict[str, Any]) -> str:
    client.request(
        "PATCH",
        "/api/accounts/profile/",
        json_body={"first_name": f"E2E-{state['run_id']}"},
        expected=(200,),
    )
    response = client.request(
        "POST",
        "/api/accounts/addresses/",
        json_body={
            "name": f"E2E Address {state['run_id']}",
            "address_line_1": "123 Test Street",
            "city": "Nairobi",
            "state_province": "Nairobi",
            "postal_code": "00100",
            "country": "Kenya",
            "is_default": True,
        },
        expected=(201,),
    )
    payload = read_json(response)
    return f"address created id={payload.get('id')}"


def admin_module_views(client: Client, state: Dict[str, Any]) -> str:
    del state
    endpoints = [
        "/api/accounts/management/",
        "/api/platform_settings/features/",
        "/api/platform_settings/admin-users/",
        "/api/platform_settings/roles/",
        "/api/platform_settings/payment-gateways/",
        "/api/platform_settings/exchange-rate-configs/",
        "/api/rbac/audit-logs/",
        "/api/security/violations/",
    ]
    for path in endpoints:
        client.request("GET", path, expected=(200,))
    return "admin list endpoints responded"


def admin_create_managed_user(client: Client, state: Dict[str, Any]) -> str:
    username = make_unique("e2e-user", state)
    response = client.request(
        "POST",
        "/api/accounts/management/",
        json_body={
            "email": f"{username}@example.com",
            "username": username,
            "role": "VENDOR",
            "first_name": "E2E",
            "last_name": "Managed",
        },
        expected=(201,),
    )
    payload = read_json(response)
    return f"managed user created id={payload.get('id') or payload.get('uuid')}"


def vendor_me(client: Client, state: Dict[str, Any]) -> str:
    response = client.session.get(
        f"{client.base_url}/api/vendors/me/",
        timeout=client.timeout,
    )
    if response.status_code == 403:
        client.request(
            "POST",
            "/api/vendors/",
            json_body={
                "business_name": make_unique("E2E Vendor", state),
                "registration_number": make_unique("REG", state),
                "country": resolve_country_id(client),
                "location": "Nairobi",
                "provides_delivery": True,
                "delivery_radius_km": 25,
                "categories_served": ["Cement", "Steel"],
            },
            expected=(201,),
        )
        response = client.request("GET", "/api/vendors/me/", expected=(200,))
    elif response.status_code != 200:
        raise AssertionError(
            f"GET /api/vendors/me/ returned {response.status_code}: {truncate(response.text)}"
        )
    payload = read_json(response)
    return f"vendor profile={payload.get('business_name', 'ok')}"


def vendor_inventory(client: Client, state: Dict[str, Any]) -> str:
    categories = read_json(
        client.request(
            "GET",
            "/api/taxonomy/categories/",
            params={"taxonomy_type": "MATERIAL"},
            expected=(200,),
        )
    )
    category_uuid = first_identifier(categories, keys=("uuid", "id"))
    if not category_uuid:
        raise AssertionError("No material category available for vendor product bootstrap")

    created = read_json(
        client.request(
            "POST",
            "/api/v1/products/",
            json_body={
                "category": str(category_uuid),
                "country": resolve_country_id(client),
                "name": make_unique("E2E Product", state),
                "description": "Vendor inventory bootstrap product",
                "base_price": 700,
                "unit": "bag",
                "stock_quantity": 10,
            },
            expected=(201,),
        )
    )
    product_id = created.get("id") or created.get("uuid")
    product_name = created.get("name")
    me_payload = read_json(client.request("GET", "/api/v1/products/me/", expected=(200,)))
    items = list_items(me_payload)
    product = next(
        (
            item
            for item in items
            if str(item.get("id") or item.get("uuid")) == str(product_id)
        ),
        None,
    )
    if not product:
        raise AssertionError("Newly created vendor product was not returned by /api/v1/products/me/")
    before = product.get("stock_quantity")
    client.request(
        "POST",
        f"/api/v1/products/{product_id}/adjust-inventory/",
        json_body={
            "quantity_delta": 1,
            "note": f"E2E adjustment {state['run_id']}",
            "reference": f"e2e-{state['run_id']}",
        },
        expected=(200,),
    )
    history = read_json(
        client.request(
            "GET",
            f"/api/v1/products/{product_id}/inventory-history/",
            expected=(200,),
        )
    )
    state["product_id"] = product_id
    state["product_name"] = product_name
    return f"adjusted product={product_id} from_stock={before} history_items={len(list_items(history))}"


def catalog_search_and_country_filter(client: Client, state: Dict[str, Any]) -> str:
    product_id = state.get("product_id")
    product_name = state.get("product_name")
    if not product_id or not product_name:
        raise AssertionError("catalog state missing product_id/product_name")

    kenya_results = read_json(
        client.request(
            "GET",
            "/api/v1/products/",
            params={"search": product_name, "page": 1, "page_size": 12},
            expected=(200,),
        )
    )
    kenya_ids = collect_identifiers(kenya_results)
    if str(product_id) not in kenya_ids:
        raise AssertionError(f"Catalog search did not return created product {product_id} for active country {client.country}")

    uganda_results = read_json(
        client.raw_request(
            "GET",
            "/api/v1/products/",
            params={"search": product_name, "page": 1, "page_size": 12},
            headers={"X-Active-Country": "UG"},
            expected=(200,),
        )
    )
    uganda_ids = collect_identifiers(uganda_results)
    if str(product_id) in uganda_ids:
        raise AssertionError(f"Catalog country filter leaked product {product_id} into UG results")

    return f"catalog search scoped correctly for product={product_id}"


def public_contracts(client: Client, state: Dict[str, Any]) -> str:
    del state
    response = client.request("GET", "/api/v2/contracts/", params={"status": "POSTED"}, expected=(200,))
    return f"contracts_visible={len(list_items(read_json(response)))}"


def register_contractor(client: Client, state: Dict[str, Any]) -> str:
    response = client.session.get(
        f"{client.base_url}/api/v2/contractors/me/",
        timeout=client.timeout,
    )
    if response.status_code == 200:
        payload = read_json(response)
        return f"contractor profile exists id={payload.get('id')}"
    create = client.request(
        "POST",
        "/api/v2/contractors/register/",
        json_body={
            "company_name": make_unique("E2E Contractor", state),
            "service_categories": ["General Construction"],
            "operating_region": "Nairobi",
        },
        expected=(201,),
    )
    payload = read_json(create)
    return f"contractor registered id={payload.get('id')}"


def owner_project_workflow(client: Client, state: Dict[str, Any]) -> str:
    project_title = make_unique("E2E Project", state)
    create_payload = read_json(
        client.request(
            "POST",
            "/api/projects/",
            json_body={
                "title": project_title,
                "description": "Frontend-driven E2E project flow",
                "location_text": "Westlands",
                "estimated_budget": 5000000,
                "funding_required": True,
            },
            expected=(201,),
        )
    )
    project_id = create_payload["id"]

    client.request(
        "POST",
        f"/api/projects/{project_id}/requirements/",
        json_body={
            "type": "MATERIAL",
            "description": "Cement",
            "quantity": "100 bags",
        },
        expected=(201,),
    )
    client.request(
        "POST",
        f"/api/projects/{project_id}/updates/",
        json_body={"update_text": f"E2E progress update {state['run_id']}"},
        expected=(201,),
    )
    commitments = client.request("GET", f"/api/projects/{project_id}/commitments/", expected=(200,))
    state["project_id"] = project_id
    state["project_title"] = project_title
    return f"project created id={project_id} commitments={len(read_json(commitments))}"


def project_search_and_country_filter(client: Client, state: Dict[str, Any]) -> str:
    project_id = state.get("project_id")
    project_title = state.get("project_title")
    if not project_id or not project_title:
        raise AssertionError("project state missing project_id/project_title")

    mine_results = read_json(
        client.request(
            "GET",
            "/api/projects/",
            params={"owner": "me", "search": project_title},
            expected=(200,),
        )
    )
    mine_ids = collect_identifiers(mine_results)
    if str(project_id) not in mine_ids:
        raise AssertionError(f"Project search/owner filter did not return project {project_id}")

    uganda_results = read_json(
        client.raw_request(
            "GET",
            "/api/projects/",
            params={"search": project_title},
            headers={"X-Active-Country": "UG"},
            expected=(200,),
        )
    )
    uganda_ids = collect_identifiers(uganda_results)
    if str(project_id) in uganda_ids:
        raise AssertionError(f"Project country filter leaked project {project_id} into UG results")

    return f"project search and owner/country filters passed for project={project_id}"


def investor_commitment(client: Client, state: Dict[str, Any]) -> str:
    project_id = state.get("project_id")
    if not project_id:
        raise AssertionError("project_id missing from state")
    response = client.request(
        "POST",
        f"/api/projects/{project_id}/commit/",
        json_body={"amount_committed": 1000},
        expected=(201,),
    )
    payload = read_json(response)
    return f"commitment created id={payload.get('id')}"


def property_workflow(client: Client, state: Dict[str, Any]) -> str:
    listing = read_json(
        client.request(
            "POST",
            "/api/property/",
            json_body={
                "title": make_unique("E2E Property", state),
                "description": "End-to-end property listing",
                "asset_type": "RESIDENTIAL",
                "listing_type": "SALE",
                "price_estimate": "18000000.00",
                "location_text": "Westlands, Nairobi",
                "specification": {
                    "bedrooms": 3,
                    "bathrooms": 2,
                    "internal_area": "190.00",
                    "internal_area_unit": "SQM",
                },
                "pricing_profile": {
                    "currency": "KES",
                    "asking_price": "18000000.00",
                    "pricing_strategy": "NEGOTIABLE",
                },
                "features": [
                    {"name": "Backup Generator", "category": "Utilities", "is_highlighted": True}
                ],
            },
            expected=(201,),
        )
    )
    property_id = listing["id"]
    property_title = listing["title"]
    window = read_json(
        client.request(
            "POST",
            "/api/property/availability-windows/",
            json_body={
                "property": property_id,
                "start_at": "2026-06-01T09:00:00Z",
                "end_at": "2026-06-01T12:00:00Z",
                "slot_duration_minutes": 60,
            },
            expected=(201,),
        )
    )
    state["property_id"] = property_id
    state["property_title"] = property_title
    state["availability_window_id"] = window["id"]
    return f"property created id={property_id} window={window['id']}"


def property_search_and_country_filter(client: Client, state: Dict[str, Any]) -> str:
    property_id = state.get("property_id")
    property_title = state.get("property_title")
    if not property_id or not property_title:
        raise AssertionError("property state missing property_id/property_title")

    kenya_results = read_json(
        client.request(
            "GET",
            "/api/property/",
            params={"search": property_title},
            expected=(200,),
        )
    )
    kenya_ids = collect_identifiers(kenya_results)
    if str(property_id) not in kenya_ids:
        raise AssertionError(f"Property search did not return property {property_id}")

    uganda_results = read_json(
        client.raw_request(
            "GET",
            "/api/property/",
            params={"search": property_title},
            headers={"X-Active-Country": "UG"},
            expected=(200,),
        )
    )
    uganda_ids = collect_identifiers(uganda_results)
    if str(property_id) in uganda_ids:
        raise AssertionError(f"Property country filter leaked property {property_id} into UG results")

    return f"property search and country filter passed for property={property_id}"


def anonymous_property_leads(client: Client, state: Dict[str, Any]) -> str:
    property_id = state.get("property_id")
    window_id = state.get("availability_window_id")
    if not property_id or not window_id:
        raise AssertionError("property workflow state missing")
    client.request(
        "POST",
        "/api/property/inquiries/",
        json_body={
            "property": property_id,
            "full_name": "Anonymous Visitor",
            "email": f"visitor-{state['run_id']}@example.com",
            "message": "I would like more details.",
        },
        expected=(201,),
    )
    appointment = read_json(
        client.request(
            "POST",
            "/api/property/appointments/",
            json_body={
                "property": property_id,
                "availability_window": window_id,
                "full_name": "Prospective Buyer",
                "phone_number": "+254700000000",
                "scheduled_start": "2026-06-01T09:00:00Z",
                "scheduled_end": "2026-06-01T10:00:00Z",
            },
            expected=(201,),
        )
    )
    return f"anonymous appointment id={appointment.get('id')}"


def notifications_preferences(client: Client, state: Dict[str, Any]) -> str:
    del state
    current = read_json(client.request("GET", "/api/notifications/preferences/", expected=(200,)))
    updated = read_json(
        client.request(
            "PATCH",
            "/api/notifications/preferences/",
            json_body={
                "email_enabled": not bool(current.get("email_enabled", True)),
                "sms_enabled": True,
            },
            expected=(200,),
        )
    )
    return f"notification prefs updated email_enabled={updated.get('email_enabled')}"


def module_sweep(client: Client, state: Dict[str, Any]) -> str:
    del state
    endpoints = [
        "/api/vendors/",
        "/api/orders/",
        "/api/orders/quote-requests/",
        "/api/reviews/ratings/",
        "/api/v2/contractors/",
        "/api/v2/contracts/",
        "/api/v2/bids/",
        "/api/milestones/",
        "/api/projects/",
        "/api/property/",
        "/api/logistics/carriers/",
        "/api/logistics/couriers/",
        "/api/logistics/pricing-zones/",
        "/api/logistics/pricing-rules/",
        "/api/logistics/shipments/",
        "/api/compliance/kyc-verifications/",
        "/api/compliance/jurisdiction-rules/",
        "/api/chat/rooms/",
        "/api/chat/messages/",
        "/api/chat/attachments/",
        "/api/v3/escrow/",
        "/api/v3/escrow-releases/",
        "/api/v3/disputes/",
        "/api/v3/finance/products/",
        "/api/v3/finance/applications/",
        "/api/v3/scoring/",
        "/api/v5/investors/",
        "/api/v5/agreements/",
        "/api/v5/organizations/",
        "/api/v5/workflows/",
        "/api/v5/tenders/",
        "/api/v5/kyc/",
        "/api/v5/risk-alerts/",
        "/api/v6/bank-accounts/",
        "/api/v6/settlements/",
        "/api/v6/regulatory-reports/",
        "/api/v6/analytics/summary/",
        "/api/v6/ai-predictions/",
        "/api/v6/secondary-trades/",
        "/api/v6/erp-connectors/",
    ]
    for path in endpoints:
        client.request("GET", path, expected=(200,))
    return f"swept {len(endpoints)} endpoints"


def build_steps(harness: Harness) -> None:
    harness.run_step(module="bootstrap", name="public-bootstrap", actor="admin", func=public_bootstrap)
    harness.run_step(module="accounts", name="profile-and-address", actor="owner", func=profile_and_address)
    harness.run_step(module="admin", name="module-views", actor="admin", func=admin_module_views)
    if harness.args.mode == "full":
        harness.run_step(module="admin", name="create-managed-user", actor="admin", func=admin_create_managed_user)
        harness.run_step(module="onboarding", name="owner-self-registration", actor="admin", func=owner_self_registration)
        harness.run_step(module="onboarding", name="vendor-admin-approval", actor="admin", func=vendor_admin_approval_onboarding)
        harness.run_step(module="onboarding", name="contractor-admin-approval", actor="admin", func=contractor_admin_approval_onboarding)
        harness.run_step(module="onboarding", name="investor-admin-approval", actor="admin", func=investor_admin_approval_onboarding)
        harness.run_step(module="onboarding", name="courier-role-approval", actor="admin", func=courier_admin_approval_onboarding)
        harness.run_step(module="onboarding", name="government-role-approval", actor="admin", func=government_admin_approval_onboarding)
    harness.run_step(module="vendors", name="vendor-me", actor="vendor", func=vendor_me)
    harness.run_step(module="catalog", name="vendor-inventory", actor="vendor", func=vendor_inventory)
    harness.run_step(module="catalog", name="search-and-country-filter", actor="vendor", func=catalog_search_and_country_filter)
    harness.run_step(module="contracts", name="public-contracts", actor="admin", func=public_contracts)
    if harness.args.mode == "full":
        harness.run_step(module="contractors", name="register-contractor", actor="contractor", func=register_contractor)
        harness.run_step(module="projects", name="owner-project-workflow", actor="owner", func=owner_project_workflow)
        harness.run_step(module="projects", name="search-and-country-filter", actor="owner", func=project_search_and_country_filter)
        harness.run_step(module="projects", name="investor-commitment", actor="investor", func=investor_commitment)
        harness.run_step(module="property", name="owner-property-workflow", actor="owner", func=property_workflow)
        harness.run_step(module="property", name="search-and-country-filter", actor="owner", func=property_search_and_country_filter)
        harness.run_step(module="property", name="anonymous-leads", actor="admin", func=anonymous_property_leads)
        harness.run_step(module="notifications", name="preferences", actor="owner", func=notifications_preferences)
    harness.run_step(module="sweep", name="module-sweep", actor="admin", func=module_sweep)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Marketplace API-only Python E2E harness"
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--country", default=DEFAULT_COUNTRY)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--startup-wait", type=float, default=DEFAULT_STARTUP_WAIT)
    parser.add_argument("--retry-delay", type=float, default=DEFAULT_RETRY_DELAY)
    parser.add_argument("--mode", choices=("smoke", "full"), default="full")
    parser.add_argument("--module", action="append", default=[], help="Run only the named module")
    parser.add_argument("--fail-fast", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    harness = Harness(args)
    build_steps(harness)
    return harness.summary()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
