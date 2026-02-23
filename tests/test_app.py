from copy import deepcopy
import src.app as app_module


def test_get_activities_returns_all_activities(client):
    # Arrange
    baseline = deepcopy(app_module.activities)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    assert resp.json() == baseline


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "testuser@example.com"
    assert email not in app_module.activities[activity_name]["participants"]

    # Act
    resp = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in app_module.activities[activity_name]["participants"]
    assert email in resp.json().get("message", "")


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = app_module.activities[activity_name]["participants"][0]

    # Act
    resp = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert resp.status_code == 400
    assert resp.json().get("detail") == "Student already signed up for this activity"


def test_delete_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = app_module.activities[activity_name]["participants"][0]
    assert email_to_remove in app_module.activities[activity_name]["participants"]

    # Act
    resp = client.delete(f"/activities/{activity_name}/participants", params={"email": email_to_remove})

    # Assert
    assert resp.status_code == 200
    assert email_to_remove not in app_module.activities[activity_name]["participants"]


def test_participants_list_updates_after_signup_and_delete(client):
    # Arrange
    activity_name = "Chess Club"
    test_email = "sequence_test@example.com"
    original_count = len(app_module.activities[activity_name]["participants"])

    # Act: signup
    resp_signup = client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
    assert resp_signup.status_code == 200

    # Assert after signup
    assert test_email in app_module.activities[activity_name]["participants"]
    assert len(app_module.activities[activity_name]["participants"]) == original_count + 1

    # Act: delete
    resp_delete = client.delete(f"/activities/{activity_name}/participants", params={"email": test_email})
    assert resp_delete.status_code == 200

    # Assert after delete
    assert test_email not in app_module.activities[activity_name]["participants"]
    assert len(app_module.activities[activity_name]["participants"]) == original_count
