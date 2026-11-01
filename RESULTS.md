# API lab results

## Part 0

- Step 0.1, the number of pizza names: 19

- Step 0.3, status code of the request without a token: 401 Unauthorized

- Step 0.4, the name of your pizza: The Scary Marinara

- Step 0.12, results of the three runs without a session (optional):
  - Run 1: FAILED
  - Run 2: PASSED
  - Run 3: FAILED

- Step 0.16, blocks of "how many of the three tools are excluded":
  - B1: 0 tools excluded — `[]`
  - B2: 1 tool excluded — `["Knife"]`
  - B3: 2 tools excluded — `["Knife", "Scissors"]`
  - B4: 3 tools excluded — `["Knife", "Pizza cutter", "Scissors"]`
  - The original tests covered only B2.
  - Additional test inputs were added for B1 and B3.
  - B4 revealed a defect because the API returned HTTP 500 instead of HTTP 400.
  - The failing test was separated and marked as `xfail` to document the known defect.

---

## Defect report

- **Title:** Excluding all available pizza tools causes HTTP 500

- **Request:** POST /api/pizza
  - Authorization: Valid logged-in user token
  - Content-Type: application/json
  - Body: `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}`

- **Expected result:** HTTP 400 Bad Request with a JSON error message explaining that no pizza can satisfy the request.

- **Actual result:** HTTP 500 Internal Server Error with an empty response body.

- **Severity:** Medium

- **Explanation:** The API fails to handle a request that excludes all available cutting tools. Instead of returning a meaningful validation error, the server returns an internal error without an explanation. This makes it difficult for applications to handle the problem properly.

- **Test handling:** The defect is documented using `@pytest.mark.xfail` with `strict=True`. This preserves the test while allowing the remaining suite to run successfully. If the defect is fixed, the unexpected pass will alert us to review the test.

---

## Part A

- Step A4, status codes when the other user reads, changes and deletes:
  - GET (Read): 404 Not Found
  - PUT (Update): 400 Bad Request
  - DELETE: 400 Bad Request

All three ownership tests passed. Unauthorized operations were rejected, and the owner's rating remained unchanged.

---

## Part B

### 1. API Tests vs. Unit Tests

API tests send real requests to a running server, so they can detect failures that unit tests using stubs cannot.

First, API tests can detect communication problems, including network errors, HTTP response errors, and issues involving the actual server.

Second, API tests can detect integration problems involving authentication, load balancing, and stored data. For example, the QuickPizza lab demonstrated that registration and login may fail when requests reach different backend servers.

Unit tests with stubs are still useful because they are faster, more isolated, and easier to debug. They can test individual functions without depending on external services or network availability.

### 2. Independent Test Users

Every test creates a new user with a unique username to prevent tests from interfering with each other's data.

Using the public token for creating or modifying ratings would be unsafe because the data could be shared with other students, making the tests unreliable.

By creating separate users, each test can work with its own ratings without affecting other users.

In Project 2, I would apply the same approach to the shared shop or hotel system by creating unique test data for each test and modifying or deleting only the data created by my own tests.

This makes the tests independent and reduces interference between groups.

### 3. Why Use One Session?

We use `requests.Session()` because it preserves cookies between HTTP requests.

QuickPizza runs on multiple backend servers behind a load balancer. The AWSALB cookie helps keep requests directed to the same server.

Without a session, a user might be registered on one server while the login request reaches another server that does not recognize the new account.

In Step 0.12, I ran the test three times without a session.

My results were:

- Run 1: FAILED
- Run 2: PASSED
- Run 3: FAILED

The same test produced different results without changing the code. This demonstrates flaky testing caused by inconsistent server selection.

Using one session helps prevent this problem by preserving the load balancer's cookie.

### 4. Excluded Tools Defect

The defect was discovered in block B4, where all three cutting tools were excluded.

The excluded tools were Knife, Pizza cutter, and Scissors.

QuickPizza returned HTTP 500 Internal Server Error with an empty response body instead of HTTP 400 Bad Request with a JSON error message.

An HTTP 500 response with an empty body is worse for an application because it gives no useful explanation of why the request failed.

With HTTP 400 and a meaningful JSON error, the application could inform the user that no pizza can satisfy the selected restrictions and ask them to change their choices.

The test remains in the suite as `xfail` instead of being deleted because it documents the known defect.

Using `strict=True` also helps detect when the defect has been fixed, so the test can be updated accordingly.

### 5. Base Choice vs. All Combinations Coverage

The input domain model contains four characteristics:

- C1: Value of stars — 3 blocks
- C2: Type of stars — 4 blocks
- C3: Pizza — 2 blocks
- C4: Token — 3 blocks

**Base choice coverage:**

1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1)

= 1 + 2 + 3 + 1 + 2

= **9 tests**

**All combinations coverage:**

3 × 4 × 2 × 3

= **72 tests**

Base choice coverage requires fewer tests because it starts with one valid base test and changes only one characteristic at a time.

All combinations coverage tests every combination of blocks, so it provides broader coverage but requires significantly more tests.

### 6. Rating Ownership and Authorization

In Step A4, another user attempted to read, update, and delete a rating belonging to the original user.

The observed HTTP status codes were:

- GET (Read): 404 Not Found
- PUT (Update): 400 Bad Request
- DELETE: 400 Bad Request

I would generally expect HTTP 403 Forbidden for an authenticated user attempting to access a resource without permission.

HTTP 404 Not Found is also reasonable if the API intentionally hides the existence of another user's rating.

The observed HTTP 400 responses for PUT and DELETE are less specific than HTTP 403, but they still indicate that the requests were rejected.

This difference is not necessarily a defect because the lab requires unauthorized requests to return a status code between 400 and 499.

All three tests passed, and the original user's rating remained unchanged.

Therefore, the API enforced the ownership restrictions required by this lab, although the specific status codes could be improved for clarity.

### 7. Made-Up Authentication Token

I created `madeup.txt` with the following authorization header:

`Authorization: token 0000000000000000`

I then sent a GET request to `/api/ratings` using curl.

**Observed status:**

HTTP 200 OK

**Observed response:**

The API returned a JSON object containing a list of existing ratings, including rating IDs, star values, and pizza IDs.

**Expected result:**

HTTP 401 Unauthorized because the token was fabricated and was not obtained through a legitimate login.

**Is this a defect?**

Yes. The API accepted the fabricated token for this protected read request and returned rating data. This indicates an authentication validation problem.

In a real system, a stranger could potentially use a fabricated token to access information without logging in.

If similar authentication weaknesses existed in other endpoints, an attacker might gain unauthorized access to additional resources.

This could become a serious security vulnerability, particularly if the exposed information were private or sensitive.

This experiment demonstrates the importance of verifying authentication credentials rather than merely checking whether a token has the expected format or length.

Only a GET request was performed with the fabricated token, following the lab's restrictions. No attempt was made to create, modify, or delete data with it.

### 8. API Testing vs. Web Page Testing

API testing is better for directly verifying HTTP status codes, JSON response fields, authentication responses, and error handling.

It allows us to check the server's behavior without depending on a browser or graphical interface.

For example, API tests can verify that invalid input returns HTTP 400 and that the response contains the correct JSON error message.

Web page testing is necessary for checking visual appearance, page layout, buttons, forms, and user interactions.

For example, only a browser-based test can verify that an error message is displayed correctly to the user or that the page layout works properly.

Both testing approaches are important because API tests verify server behavior, while web page tests verify the user's experience.
