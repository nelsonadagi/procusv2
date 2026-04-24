from rbac.permission_catalog import get_role_permission_matrix


def test_property_manager_role_has_property_operator_permissions():
    matrix = get_role_permission_matrix()

    assert "PROPERTY_MANAGER" in matrix
    assert "projects:view" in matrix["PROPERTY_MANAGER"]
    assert "property:view" in matrix["PROPERTY_MANAGER"]
    assert "property:list_property" in matrix["PROPERTY_MANAGER"]
    assert "property:update_property" in matrix["PROPERTY_MANAGER"]


def test_courier_role_has_logistics_permissions():
    matrix = get_role_permission_matrix()

    assert "COURIER" in matrix
    assert "logistics:view" in matrix["COURIER"]
    assert "logistics:onboard" in matrix["COURIER"]
    assert "logistics:manage_profile" in matrix["COURIER"]
    assert "logistics:manage_pricing" in matrix["COURIER"]
    assert "logistics:manage_shipments" in matrix["COURIER"]


def test_project_owner_keeps_base_onboarding_permissions():
    matrix = get_role_permission_matrix()

    assert "PROJECT_OWNER" in matrix
    assert "contractors:view" in matrix["PROJECT_OWNER"]
    assert "investments:onboard" in matrix["PROJECT_OWNER"]
    assert "escrow:deposit_funds" in matrix["PROJECT_OWNER"]
    assert "reviews:create" in matrix["PROJECT_OWNER"]


def test_government_role_is_distinct_from_elevated_government_groups():
    matrix = get_role_permission_matrix()

    assert "government:publish_tender" in matrix["GOVERNMENT"]
    assert "government:audit_tender" not in matrix["GOVERNMENT"]
    assert "government:audit_tender" in matrix["GOVERNMENT_OWNER"]
