import hashlib


# Admin username
ADMIN_USERNAME = "admin"


# Hash password
def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# Stored hashed password
ADMIN_PASSWORD_HASH = hash_password(
    "admin123"
)


# Login function
def login():

    print("\n========== LOGIN ==========\n")

    username = input("Enter Username: ")

    password = input("Enter Password: ")

    # Hash entered password
    entered_password_hash = hash_password(
        password
    )

    # Verify credentials
    if (

        username == ADMIN_USERNAME

        and

        entered_password_hash
        ==
        ADMIN_PASSWORD_HASH
    ):

        print("\nLogin Successful!")

        return True

    else:

        print("\nInvalid Username or Password!")

        return False