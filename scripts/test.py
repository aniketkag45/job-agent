from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

print("Test 1: Existing login still works?")
# This will fail if no user but endpoint exists
resp = client.post("/login", data={"grant_type":"password","username":"aniketkagsirvi@gmail.com","password":"wrong"})
print(f"  Status: {resp.status_code} (401 expected for wrong pass) -> OK if 401")

print("\nTest 2: Google routes exist?")
for route in ["/auth/google/login"]:
    r = client.get(route, follow_redirects=False)
    print(f"  GET {route} -> {r.status_code} (302 redirect to Google expected if CLIENT_ID real, 500 if placeholder)")
    if r.status_code == 302:
        print(f"     Location: {str(r.headers.get('location'))[:100]}...")
    else:
        print(f"     Detail: {r.text[:200]}")

print("\nTest 3: POST /auth/google with fake token should 401")
r = client.post("/auth/google", json={"id_token":"fake"})
print(f"  Status: {r.status_code} (401 expected) -> {'OK' if r.status_code==401 else 'CHECK'}")

print("\nDone! Delete scripts/test.py")