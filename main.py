import importlib

from core.login import login


# =========================
# LOGIN VERIFICATION
# =========================

if not login():

    exit()


# =========================
# MENU DISPLAY
# =========================

def show_menu():

    print("\n========================================")

    print("   SECURE LAND REGISTRY SYSTEM")

    print("========================================")

    print("\n1. Register Land")

    print("2. Verify Blockchain")

    print("3. View Transaction History")

    print("4. Search Land Record")

    print("5. Compare AI Models")

    print("6. Exit")


# =========================
# MAIN LOOP
# =========================

while True:

    show_menu()

    choice = input(
        "\nEnter Your Choice: "
    )

    # =========================
    # REGISTER LAND
    # =========================

    if choice == "1":

        print(
            "\nOpening Land Registration Module...\n"
        )

        import core.land_registration

        importlib.reload(
            core.land_registration
        )

    # =========================
    # VERIFY BLOCKCHAIN
    # =========================

    elif choice == "2":

        print(
            "\nOpening Blockchain Verification...\n"
        )

        import core.land_verification

        importlib.reload(
            core.land_verification
        )

    # =========================
    # TRANSACTION HISTORY
    # =========================

    elif choice == "3":

        print(
            "\nOpening Transaction History...\n"
        )

        import core.transaction_history

        importlib.reload(
            core.transaction_history
        )

    # =========================
    # SEARCH LAND RECORD
    # =========================

    elif choice == "4":

        print(
            "\nOpening Search Module...\n"
        )

        import core.search_land

        importlib.reload(
            core.search_land
        )

    # =========================
    # AI MODEL COMPARISON
    # =========================

    elif choice == "5":

        print(
            "\nOpening AI Model Comparison...\n"
        )

        import ai_model.model_comparison

        importlib.reload(
            ai_model.model_comparison
        )

    # =========================
    # EXIT SYSTEM
    # =========================

    elif choice == "6":

        print(
            "\nSystem Closed Successfully."
        )

        print(
            "Thank You For Using "
            "Secure Land Registry System.\n"
        )

        break

    # =========================
    # INVALID INPUT
    # =========================

    else:

        print(
            "\nInvalid Choice. Please Try Again."
        )