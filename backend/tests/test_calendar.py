from app.services.meeting_service import meetings_for, tomorrow


def test_tomorrow_has_two_meetings():
    ms = meetings_for(tomorrow())
    assert {m["event_id"] for m in ms} == {"evt_abc_001", "evt_xyz_001"}
    assert ms[0]["date"] == tomorrow()
