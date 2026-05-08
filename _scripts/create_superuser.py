import users.models as UserCreation

print("[Special User Creation]")

UserCreation.create_superuser()

print("1. Django Superuser Creation Success")

UserCreation.create_court_user(
    "testcourtuser7", "court@example.com", "testpass999999", "CourtUser", "Court"
)

print("2. Court User Creation Success")