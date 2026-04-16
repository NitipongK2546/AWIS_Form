import users.models as UserFile

UserFile.create_superuser()

UserFile.create_court_user(
    "testcourtuser7", "court@example.com", "testpass999999", "CourtUser", "Court"
)

print("Success")