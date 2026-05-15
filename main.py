import importlib

from core.login import login


# Login verification
if not login():

    exit()


def show_menu():

    print("\n========================================")
    print("  SECURE LAND REGISTRATION SYSTEM")
    print("========================================")

    print("\n1. Register Land")
    print("2. Verify Blockchain")
    print("3. View Transaction History")
    print("4. Search Land Record")
    print("5. Exit")


while True:

    show_menu()

    choice = input("\nEnter Your Choice: ")

    # Register land
    if choice == "1":

        import core.land_registration

        importlib.reload(
            core.land_registration
        )

    # Verify blockchain
    elif choice == "2":

        import core.land_verification

        importlib.reload(
            core.land_verification
        )

    # Transaction history
    elif choice == "3":

        import core.transaction_history

        importlib.reload(
            core.transaction_history
        )

    # Search land
    elif choice == "4":

        import core.search_land

        importlib.reload(
            core.search_land
        )

    # Exit
    elif choice == "5":

        print("\nSystem Closed Successfully")

        break

    # Invalid choice
    else:

        print("\nInvalid Choice. Try Again.")