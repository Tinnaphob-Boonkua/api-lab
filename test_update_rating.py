
import pytest

# Rating updates accept 1 and 5, reject 0 and 6,
# and rejected updates must not change the saved rating.
@pytest.mark.parametrize("stars, expected_status", [
    (0, 400),
    (1, 200),
    (5, 200),
    (6, 400),
])
def test_update_rating_boundaries(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"

    # Attempt to update the rating.
    res = api.put(path, json={"stars": stars}, headers=auth)

    # Check the status code.
    assert res.status_code == expected_status

    # Read the rating again.
    saved = api.get(path, headers=auth)
    assert saved.status_code == 200

    # Valid updates are saved; invalid updates leave 3 stars.
    if expected_status == 200:
        assert res.json()["stars"] == stars
        assert saved.json()["stars"] == stars
    else:
        assert saved.json()["stars"] == 3
