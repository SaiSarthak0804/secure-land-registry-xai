import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

from core.login import hash_password

from database.db_connect import connection

from blockchain.blockchain import Blockchain

from blockchain.block import Block

from ai_model.fraud_checker import check_fraud

from ai_model.shap_explainer import generate_xai

from blockchain.digital_signature import (
    generate_signature,
    verify_signature
)

app = Flask(__name__)

app.secret_key = "secure_land_registry"

land_chain = Blockchain()

# =========================
# ADMIN LOGIN
# =========================

ADMIN_USERNAME = "admin"

ADMIN_PASSWORD_HASH = hash_password(
    "admin123"
)

# =========================
# LOGIN PAGE
# =========================

@app.route("/", methods=["GET", "POST"])

def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        entered_password_hash = hash_password(
            password
        )

        if (
            username == ADMIN_USERNAME
            and
            entered_password_hash == ADMIN_PASSWORD_HASH
        ):

            session["user"] = username

            return redirect(
                url_for("dashboard")
            )

        else:

            error = "Invalid Username or Password"

    return render_template(
        "login.html",
        error=error
    )

# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")

def dashboard():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    cursor = connection.cursor()

    # Total Records
    cursor.execute(
        "SELECT COUNT(*) FROM land_records"
    )

    total_records = cursor.fetchone()[0]

    # Fraud Count
    cursor.execute(
        "SELECT COUNT(*) FROM fraud_logs"
    )

    fraud_count = cursor.fetchone()[0]

    cursor.close()

    blockchain_status = "VALID"

    ai_status = "ACTIVE"

    return render_template(

        "dashboard.html",

        total_records=total_records,

        fraud_count=fraud_count,

        blockchain_status=blockchain_status,

        ai_status=ai_status
    )

# =========================
# REGISTER LAND
# =========================

@app.route("/register", methods=["GET", "POST"])

def register_land():

    result = None

    shap_image = False

    if request.method == "POST":

        owner_name = request.form["owner_name"]

        land_id = request.form["land_id"]

        location = request.form["location"]

        area = float(
            request.form["area"]
        )

        transaction_count = int(
            request.form["transaction_count"]
        )

        market_value = int(
            request.form["market_value"]
        )

        owner_history = int(
            request.form["owner_history"]
        )

        cursor = connection.cursor()

        # Duplicate check
        check_query = """
        SELECT * FROM land_records
        WHERE land_id = %s
        """

        cursor.execute(
            check_query,
            (land_id,)
        )

        existing_land = cursor.fetchone()

        if existing_land:

            result = (
                "Duplicate Land ID Detected!"
            )

        else:

            # =========================
            # AI FRAUD DETECTION FIRST
            # =========================

            is_fraud, reason, confidence = check_fraud(

                area,

                transaction_count,

                market_value,

                owner_history
            )

            # =========================
            # BLOCK FRAUD USERS
            # =========================

            if confidence >= 70:

                result = (

                    f"Registration BLOCKED | "

                    f"{reason} | "

                    f"Fraud Confidence: "

                    f"{confidence}%"
                )

            else:

                # =========================
                # INSERT RECORD
                # =========================

                insert_query = """
                INSERT INTO land_records
                (
                    owner_name,
                    land_id,
                    location,
                    area
                )
                VALUES (%s, %s, %s, %s)
                """

                cursor.execute(

                    insert_query,

                    (
                        owner_name,
                        land_id,
                        location,
                        area
                    )
                )

                connection.commit()

                # =========================
                # BLOCKCHAIN DATA
                # =========================

                block_data = (

                    f"{land_id} | "

                    f"{owner_name} | "

                    f"{location} | "

                    f"{area}"
                )

                # =========================
                # CREATE BLOCKCHAIN BLOCK
                # =========================

                new_block = Block(

                    len(land_chain.chain),

                    block_data,

                    land_chain.get_latest_block().hash
                )

                land_chain.add_block(
                    new_block
                )

                # =========================
                # DIGITAL SIGNATURE
                # =========================

                signature = generate_signature(
                    block_data
                )

                verified = verify_signature(

                    block_data,

                    signature
                )

                # =========================
                # SHAP XAI
                # =========================

                generate_xai(

                    area,

                    transaction_count,

                    market_value,

                    owner_history
                )

                shap_image = True

                # =========================
                # FINAL RESULT
                # =========================

                result = (

                    f"Land Registered Successfully | "

                    f"{reason} | "

                    f"Fraud Confidence: "

                    f"{confidence}% | "

                    f"Digital Signature Verified: "

                    f"{verified}"
                )

        cursor.close()

    return render_template(

        "register.html",

        result=result,

        shap_image=shap_image
    )

# =========================
# SEARCH LAND
# =========================

@app.route("/search", methods=["GET", "POST"])

def search_land():

    record = None

    error = None

    if request.method == "POST":

        land_id = request.form["land_id"]

        cursor = connection.cursor()

        query = """
        SELECT * FROM land_records
        WHERE land_id = %s
        """

        cursor.execute(
            query,
            (land_id,)
        )

        record = cursor.fetchone()

        if not record:

            error = "No Land Record Found!"

        cursor.close()

    return render_template(

        "search.html",

        record=record,

        error=error
    )

# =========================
# TRANSACTION HISTORY
# =========================

@app.route("/history")

def history():

    cursor = connection.cursor()

    query = """
    SELECT
        owner_name,
        land_id,
        location,
        area,
        registration_date
    FROM land_records
    ORDER BY registration_date DESC
    """

    cursor.execute(query)

    records = cursor.fetchall()

    fraud_query = """
    SELECT COUNT(*) FROM fraud_logs
    """

    cursor.execute(fraud_query)

    fraud_count = cursor.fetchone()[0]

    cursor.close()

    return render_template(

        "history.html",

        records=records,

        fraud_count=fraud_count
    )

# =========================
# BLOCKCHAIN VERIFICATION
# =========================

@app.route("/verify")

def verify_blockchain():

    verification_chain = Blockchain()

    cursor = connection.cursor()

    query = """
    SELECT owner_name, land_id, location, area
    FROM land_records
    ORDER BY id
    """

    cursor.execute(query)

    records = cursor.fetchall()

    for record in records:

        owner_name = record[0]

        land_id = record[1]

        location = record[2]

        area = record[3]

        block_data = (

            f"{land_id} | "

            f"{owner_name} | "

            f"{location} | "

            f"{area}"
        )

        new_block = Block(

            len(verification_chain.chain),

            block_data,

            verification_chain.get_latest_block().hash
        )

        verification_chain.add_block(
            new_block
        )

    valid = verification_chain.validate_chain()

    cursor.close()

    return render_template(

        "blockchain.html",

        valid=valid
    )

# =========================
# AI MODEL COMPARISON
# =========================

@app.route("/models")

def compare_models():

    data = pd.read_csv(
        "datasets/land_fraud_dataset.csv"
    )

    X = data[
        [
            "area",
            "transaction_count",
            "market_value",
            "owner_history"
        ]
    ]

    y = data["fraud"]

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,
        test_size=0.2,
        random_state=42
    )

    models = {

        "Decision Tree":
        DecisionTreeClassifier(),

        "Logistic Regression":
        LogisticRegression(),

        "Random Forest":
        RandomForestClassifier()
    }

    results = []

    for name, model in models.items():

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        accuracy = round(
            accuracy * 100,
            2
        )

        results.append(
            (name, accuracy)
        )

    return render_template(

        "models.html",

        results=results
    )

# =========================
# LOGOUT
# =========================

@app.route("/logout")

def logout():

    session.clear()

    return redirect(
        url_for("login")
    )

# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(debug=True)