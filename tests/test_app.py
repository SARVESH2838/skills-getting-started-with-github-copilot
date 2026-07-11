import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from app import activities, app


client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]

    try:
        email = original_participants[0]

        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants
