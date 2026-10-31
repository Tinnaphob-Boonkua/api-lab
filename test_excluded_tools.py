import pytest


# The pizza never needs a tool that the customer excluded.

@pytest.mark.parametrize("excluded", [
    [],
    ["Knife"],
    ["Scissors"],
    ["Knife", "Scissors"]
])

def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded

@pytest.mark.xfail(
    reason="Defect 1: Excluding all three tools returns 500 instead of 400",
    strict=True
)

# Excluding all available tools should return 400 with a JSON error.
def test_excluding_all_tools_is_refused(api, auth):
    body = {
        "excludedTools": ["Knife", "Pizza cutter", "Scissors"]
    }

    res = api.post("/api/pizza", json=body, headers=auth)

    assert res.status_code == 400
    response = res.json()
    assert isinstance(response.get("error"), str)
    assert response["error"] != ""
