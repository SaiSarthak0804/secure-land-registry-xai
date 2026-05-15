ADMIN_USERNAME = "admin"

ADMIN_PASSWORD = "admin123"


def login():

    print("\n========== LOGIN ==========\n")

    username = input("Enter Username: ")

    password = input("Enter Password: ")

    # Correct credentials
    if (

        username == ADMIN_USERNAME

        and

        password == ADMIN_PASSWORD
    ):

        print("\nLogin Successful!")

        return True

    # Wrong credentials
    else:

        print("\nInvalid Username or Password!")

        return False