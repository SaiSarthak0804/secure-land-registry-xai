from werkzeug.security import check_password_hash

from database.db_connect import connection


# =========================
# LOGIN FUNCTION
# =========================

def login():

    print("\n========== USER LOGIN ==========\n")

    username = input(
        "Enter Username: "
    )

    password = input(
        "Enter Password: "
    )

    # =========================
    # DATABASE CURSOR
    # =========================

    cursor = connection.cursor()

    # =========================
    # FETCH USER
    # =========================

    query = """
    SELECT username, password_hash
    FROM users
    WHERE username = %s
    """

    cursor.execute(
        query,
        (username,)
    )

    user = cursor.fetchone()

    # =========================
    # VERIFY PASSWORD
    # =========================

    if user:

        stored_hash = user[1]

        if check_password_hash(
            stored_hash,
            password
        ):

            print(
                "\nLogin Successful!"
            )

            print(
                f"Welcome, {username}"
            )

            cursor.close()

            return True

    # =========================
    # INVALID LOGIN
    # =========================

    print(
        "\nInvalid Username or Password!"
    )

    cursor.close()

    return False