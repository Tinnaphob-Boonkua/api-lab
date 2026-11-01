# API lab results
## Part 0
- Step 0.1, the number of pizza names: 19
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: The Scary Marinara
- Step 0.12, results of the three runs without a session (optional):
  - Run 1: FAILED
  - Run 2: PASSED
  - Run 3: FAILED
- Step 0.16, blocks of "how many of the three tools are excluded":
    - B1: 0 tools excluded — []
    - B2: 1 tool excluded — ["Knife"]
    - B3: 2 tools excluded — ["Knife", "Scissors"]
    - B4: 3 tools excluded — ["Knife", "Pizza cutter", "Scissors"]
    - The original tests covered only B2 (1 tool excluded).
    - Added test inputs for B1 and B3 to achieve coverage of the valid cases.
    - B4 revealed a defect: the API returned HTTP 500 instead of HTTP 400.
    - The B4 test was separated and marked xfail because it exposes a known defect.
## Defect report
- Title: Excluding all available pizza tools causes HTTP 500
- Request: POST /api/pizza
    - Body: {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    - Authorization: Valid token
- Expected result: HTTP 400 with a JSON error message explaining that no pizza can satisfy the request.
- Actual result: HTTP 500 Internal Server Error with an empty response body.
- Severity: Medium. The API fails to handle an invalid request gracefully and provides no useful error message to the client.
## Part A
- Step A4, status codes when the other user reads, changes and deletes:
  - GET (Read): 404
  - PUT (Update): 400
  - DELETE: 400
## Part B
1.
2.
3.
4.
5.
6.
7.
8.