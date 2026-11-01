# api-lab
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
| C1: Below 1 | test_stars_out_of_range[0] |
| C1: Valid 1–5 | test_base_choice_is_saved |
| C1: Above 5 | test_stars_out_of_range[6] |
| C2: Whole number | test_base_choice_is_saved |
| C2: Decimal | test_stars_wrong_type (3.5) |
| C2: Text | test_stars_wrong_type ("3") |
| C2: Missing | test_missing_stars |
| C3: Existing pizza | test_base_choice_is_saved |
| C3: Nonexistent pizza | test_nonexistent_pizza |
| C4: Own token | test_base_choice_is_saved |
| C4: No token | test_rating_without_token |
| C4: Wrong-length token | test_rating_short_token |

Base choice coverage requires 9 test cases.

Calculation:
1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 9
