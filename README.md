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