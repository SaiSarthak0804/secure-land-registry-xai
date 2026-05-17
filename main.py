import importlib

from core.login import login


# Login verification
if not login():

    exit()


# Menu display
def show_menu():

    print("\n========================================")
    print("  SECURE LAND REGISTRATION SYSTEM")
    print("========================================")

    print("\n1. Register Land")
    print("2. Verify Blockchain")
    print("3. View Transaction History")
    print("4. Search Land Record")
    print("5. Compare AI Models")
    print("6. Exit")


# Main loop
while True:

    show_menu()

    choice = input("\nEnter Your Choice: ")

    # Register Land
    if choice == "1":

        import core.land_registration

        importlib.reload(
            core.land_registration
        )

    # Verify Blockchain
    elif choice == "2":

        import core.land_verification

        importlib.reload(
            core.land_verification
        )

    # View Transaction History
    elif choice == "3":

        import core.transaction_history

        importlib.reload(
            core.transaction_history
        )

    # Search Land Record
    elif choice == "4":

        import core.search_land

        importlib.reload(
            core.search_land
        )

    # Compare AI Models
    elif choice == "5":

        import ai_model.model_comparison

        importlib.reload(
            ai_model.model_comparison
        )

    # Exit
    elif choice == "6":

        print("\nSystem Closed Successfully")

        break

    # Invalid Choice
    else:

        print("\nInvalid Choice. Try Again.")