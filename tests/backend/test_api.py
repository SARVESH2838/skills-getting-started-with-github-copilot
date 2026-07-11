import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from app import activities, app


client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_catalog():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in payload
    assert payload[expected_activity]["description"]


def test_signup_and_unregister_flow_updates_participants():
    # Arrange
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]
    test_email = "backend.test@mergington.edu"

    try:
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email},
        )

        # Assert
        assert signup_response.status_code == 200
        assert test_email in activities[activity_name]["participants"]
        assert signup_response.json()["message"] == f"Signed up {test_email} for {activity_name}"

        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": test_email},
        )

        # Assert
        assert unregister_response.status_code == 200
        assert test_email not in activities[activity_name]["participants"]
        assert unregister_response.json()["message"] == f"Removed {test_email} from {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants
