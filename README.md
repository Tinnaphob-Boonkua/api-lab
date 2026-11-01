# api-lab

## ITCS386 — Software Verification and Validation

### API Testing with pytest and requests

This repository contains automated API tests for the QuickPizza API at https://quickpizza.grafana.com.

The lab demonstrates API testing using Python, pytest, requests, input space partitioning, boundary value analysis, authentication testing, CRUD operations, and defect reporting.

## Requirements

- Python 3.10 or newer
- Git
- curl
- Python packages: pytest, requests, pytest-html

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/api-lab.git
cd api-lab
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Tests

Run all automated tests:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest -v test_create_rating.py
```

Generate an HTML test report:

```bash
pytest -v --html=report.html --self-contained-html
```

Open `report.html` in a browser to view the results.

The expected complete test suite result is **32 passed, 1 xfailed**, including the known API defect.

## Test Organization

| File | Purpose |
|---|---|
| `test_names.py` | Test the list of pizza names |
| `test_tools.py` | Test authenticated access to cutting tools |
| `test_pizza.py` | Test vegetarian pizza recommendations and authentication |
| `test_users.py` | Test new user registration and initial ratings |
| `test_ratings.py` | Test creating, reading, updating, and deleting ratings |
| `test_refused.py` | Test invalid registration and login requests |
| `test_excluded_tools.py` | Test excluded tools and document a known API defect |
| `test_create_rating.py` | Test rating creation using input space partitioning |
| `test_update_rating.py` | Test rating updates using boundary values |
| `test_rating_owner.py` | Test authorization and rating ownership |
| `conftest.py` | Shared fixtures for sessions, authentication, pizzas, and ratings |

## Test Independence

The tests use pytest fixtures to create their own test data.

Each test that requires authentication creates a new user with a unique username generated using `uuid.uuid4()`.

A shared `requests.Session` preserves cookies so requests reach the same QuickPizza backend server.

The `rating` fixture creates a rating before the test and performs cleanup afterward.

This design helps prevent tests from interfering with each other and allows them to run independently.

---

## Part A — Input Domain Model

### Operation: POST /api/ratings

The API accepts a rating with a valid pizza ID, a whole number of stars between 1 and 5, and an authentication token belonging to a logged-in user.

| Characteristic | Blocks | Test values |
|---|---|---|
| C1: Value of stars | Below 1, 1–5 (base), above 5 | 0, 3, 6 |
| C2: Type of stars | Whole number (base), decimal, text, missing | 3, 3.5, "3", no field |
| C3: Pizza | Exists (base), does not exist | A new pizza, 999999999 |
| C4: Token | User's own (base), none, wrong length | From auth fixture, no header, token short |

### Test Design Method

We use base choice coverage. First, we select one valid base block for each characteristic:

- C1: 3 stars
- C2: Whole number
- C3: Existing pizza
- C4: Valid user token

We then change one characteristic at a time while keeping the other characteristics at their base values.

This method reduces the number of tests while covering every block of each characteristic.

### Base Choice Coverage

| Block | Covering Test |
|---|---|
| C1: Below 1 | `test_stars_out_of_range[0]` |
| C1: Valid 1–5 | `test_base_choice_is_saved` |
| C1: Above 5 | `test_stars_out_of_range[6]` |
| C2: Whole number | `test_base_choice_is_saved` |
| C2: Decimal | `test_stars_wrong_type` (3.5) |
| C2: Text | `test_stars_wrong_type` ("3") |
| C2: Missing | `test_missing_stars` |
| C3: Existing pizza | `test_base_choice_is_saved` |
| C3: Nonexistent pizza | `test_nonexistent_pizza` |
| C4: Own token | `test_base_choice_is_saved` |
| C4: No token | `test_rating_without_token` |
| C4: Wrong-length token | `test_rating_short_token` |

### Coverage Calculation

The model contains four characteristics with 3, 4, 2, and 3 blocks respectively.

**Base choice coverage:**

1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = **9 test cases**

**All combinations coverage:**

3 × 4 × 2 × 3 = **72 test cases**

Base choice coverage requires fewer tests because it changes only one characteristic at a time while keeping the others at their base values.

### Boundary Value Testing

For updating a rating using `PUT /api/ratings/{id}`, the accepted range is 1 to 5 stars.

The tests use four boundary values:

| Stars | Expected HTTP Status | Expected Stored Value |
|---|---|---|
| 0 | 400 Bad Request | 3 (unchanged) |
| 1 | 200 OK | 1 |
| 5 | 200 OK | 5 |
| 6 | 400 Bad Request | 3 (unchanged) |

Every test begins with a rating containing 3 stars.

The tests also read the rating after the update to verify that rejected updates do not change the saved data.

### Rating Ownership Testing

Two separate users are created to test authorization.

The first user owns a rating, while the second user attempts to access it.

| Operation | Observed HTTP Status | Result |
|---|---|---|
| GET | 404 Not Found | Refused |
| PUT | 400 Bad Request | Refused |
| DELETE | 400 Bad Request | Refused |

All three requests were rejected with 4xx status codes.

The owner's rating remained accessible and unchanged.

---

## Known API Defect

### Defect 1 — Excluding All Cutting Tools

**Endpoint:** `POST /api/pizza`

**Request body:**

```json
{
  "excludedTools": [
    "Knife",
    "Pizza cutter",
    "Scissors"
  ]
}
```

**Expected result:**

HTTP 400 Bad Request with a JSON error message explaining that no pizza can satisfy the request.

**Observed result:**

HTTP 500 Internal Server Error with an empty response body.

**Severity:** Medium

**Explanation:**

When all three available tools are excluded, QuickPizza cannot recommend a pizza. The API should return a client error explaining the invalid request rather than an internal server error.

The defect is preserved in the automated test suite using `@pytest.mark.xfail` with `strict=True`.

This allows the known defect to remain documented while alerting us if the behavior changes or the defect is fixed.

Further observations and the complete defect report are recorded in `RESULTS.md`.

## API Security Testing

The lab also includes authentication and authorization checks.

These cover missing tokens, invalid token lengths, invalid login credentials, and attempts to access another user's ratings.

The reflection section in `RESULTS.md` documents an additional authentication concern: the QuickPizza demo API returned rating data when accessed using a fabricated 16-character token.

The lab's restriction on using the made-up token for read requests only was followed.

## Files and Reports

- `README.md` — Project documentation, setup instructions, and test design
- `RESULTS.md` — Observations, defect report, and Part B reflection
- `requirements.txt` — Required Python packages
- `report.html` — HTML report generated from the complete pytest suite
- `auth.txt` — Public practice authorization header
- `veg.json` — Vegetarian pizza request body
- `madeup.txt` — Fabricated token used for the read-only authentication experiment
- `excluded_all.json` — Request body used to reproduce the excluded-tools defect

## References

- [QuickPizza API](https://quickpizza.grafana.com)
- [pytest Documentation](https://docs.pytest.org)
- [Python requests Documentation](https://requests.readthedocs.io)
- ITCS386 — API Testing with pytest and requests, Lab Exercise Version 2.0
