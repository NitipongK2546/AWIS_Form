def create_superuser():
    from django.contrib.auth import get_user_model
    
    User = get_user_model()

    user = User.objects.filter(
        username="admin",
    ).first()

    if user:
        return

    user = User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass999999"
    )

    user.first_name = "Mr. Admin"
    user.last_name = "Superuser"
    user.save()