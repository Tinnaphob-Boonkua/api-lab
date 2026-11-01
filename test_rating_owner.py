
# Another user must not read the owner's rating.
def test_other_user_cannot_read(api, auth, rating, other_auth):
    path = f"/api/ratings/{rating['id']}"

    res = api.get(path, headers=other_auth)
    print(f"Other user GET status: {res.status_code}")

    assert 400 <= res.status_code <= 499

    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json() == rating


# Another user must not modify the owner's rating.
def test_other_user_cannot_update(api, auth, rating, other_auth):
    path = f"/api/ratings/{rating['id']}"

    res = api.put(
        path,
        json={"stars": 4},
        headers=other_auth
    )
    print(f"Other user PUT status: {res.status_code}")

    assert 400 <= res.status_code <= 499

    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json() == rating
    assert owner_res.json()["stars"] == 3


# Another user must not delete the owner's rating.
def test_other_user_cannot_delete(api, auth, rating, other_auth):
    path = f"/api/ratings/{rating['id']}"

    res = api.delete(path, headers=other_auth)
    print(f"Other user DELETE status: {res.status_code}")

    assert 400 <= res.status_code <= 499

    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
    assert owner_res.json() == rating
