import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

from sklearn.preprocessing import LabelEncoder

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
# SIGNUP PAGE
# =========================

@app.route("/signup", methods=["GET", "POST"])

def signup():

    error = None

    if request.method == "POST":

        full_name = request.form["full_name"]

        email = request.form["email"]

        phone = request.form["phone"]

        username = request.form["username"]

        password = request.form["password"]

        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            error = "Passwords do not match!"

            return render_template(
                "signup.html",
                error=error
            )

        cursor = connection.cursor()

        query = """
        SELECT * FROM users
        WHERE username = %s
        OR email = %s
        """

        cursor.execute(
            query,
            (username, email)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            error = "Username or Email already exists!"

            cursor.close()

            return render_template(
                "signup.html",
                error=error
            )

        hashed_password = generate_password_hash(
            password
        )

        insert_query = """
        INSERT INTO users
        (
            full_name,
            email,
            phone,
            username,
            password_hash
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(

            insert_query,

            (
                full_name,
                email,
                phone,
                username,
                hashed_password
            )
        )

        connection.commit()

        cursor.close()

        return redirect(
            url_for("login")
        )

    return render_template(
        "signup.html",
        error=error
    )

# =========================
# LOGIN PAGE
# =========================

@app.route("/", methods=["GET", "POST"])

@app.route("/login", methods=["GET", "POST"])

def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        cursor = connection.cursor()

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

        cursor.close()

        if user:

            stored_username = user[0]

            stored_password_hash = user[1]

            if check_password_hash(

                stored_password_hash,

                password
            ):

                session["user"] = stored_username

                return redirect(
                    url_for("dashboard")
                )

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

    cursor.execute(
        "SELECT COUNT(*) FROM land_records"
    )

    total_records = cursor.fetchone()[0]

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

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    result = None

    shap_image = False

    fraud_message = None

    if request.method == "POST":

        # =========================
        # OWNER DETAILS
        # =========================

        owner_name = request.form["owner_name"]

        aadhaar_number = request.form["aadhaar_number"]

        phone_number = request.form["phone_number"]

        address = request.form["address"]

        # =========================
        # LAND DETAILS
        # =========================

        land_id = request.form["land_id"]

        survey_number = request.form["survey_number"]

        district = request.form["district"]

        state = request.form["state"]

        land_type = request.form["land_type"]

        location = request.form["location"]

        area = float(
            request.form["area"]
        )

        # =========================
        # FRAUD ANALYSIS DETAILS
        # =========================

        transaction_count = int(
            request.form["transaction_count"]
        )

        market_value = int(
            request.form["market_value"]
        )

        owner_history = int(
            request.form["owner_history"]
        )

        transfer_frequency = int(
            request.form["transfer_frequency"]
        )

        verification_status = request.form[
            "verification_status"
        ]

        cursor = connection.cursor()

        # =========================
        # DUPLICATE LAND CHECK
        # =========================

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
            # AI FRAUD DETECTION
            # =========================

            is_fraud, reason, confidence = check_fraud(

                area,

                transaction_count,

                market_value,

                owner_history,

                transfer_frequency,

                district,

                land_type,

                verification_status
            )

            # =========================
            # INSERT LAND RECORD
            # =========================

            insert_query = """
            INSERT INTO land_records
            (
                owner_name,
                land_id,
                location,
                area,
                aadhaar_number,
                phone_number,
                address,
                survey_number,
                district,
                state,
                land_type,
                transfer_frequency,
                verification_status
            )
            VALUES
            (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            """

            cursor.execute(

                insert_query,

                (
                    owner_name,
                    land_id,
                    location,
                    area,
                    aadhaar_number,
                    phone_number,
                    address,
                    survey_number,
                    district,
                    state,
                    land_type,
                    transfer_frequency,
                    verification_status
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
            # CREATE BLOCK
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
            # STORE FRAUD LOG
            # =========================

            if is_fraud:

                fraud_query = """
                INSERT INTO fraud_logs
                (
                    land_id,
                    owner_name,
                    fraud_reason
                )
                VALUES (%s, %s, %s)
                """

                cursor.execute(

                    fraud_query,

                    (
                        land_id,
                        owner_name,
                        reason
                    )
                )

                connection.commit()

                fraud_message = (

                    f"Suspicious Transaction Detected! "

                    f"Fraud Confidence: "

                    f"{confidence}%"
                )

            # =========================
            # SHAP EXPLAINABILITY
            # =========================

            generate_xai(

                area,

                transaction_count,

                market_value,

                owner_history,

                transfer_frequency,

                district,

                land_type,

                verification_status
            )

            shap_image = True

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

        fraud_message=fraud_message,

        shap_image=shap_image
    )
# =========================
# SEARCH LAND
# =========================

@app.route("/search", methods=["GET", "POST"])

def search_land():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

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

    if "user" not in session:

        return redirect(
            url_for("login")
        )

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
# FRAUD LOGS
# =========================

@app.route("/fraud-logs")

def fraud_logs():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    cursor = connection.cursor()

    query = """
    SELECT
        land_id,
        owner_name,
        fraud_reason
    FROM fraud_logs
    ORDER BY id DESC
    """

    cursor.execute(query)

    fraud_records = cursor.fetchall()

    cursor.close()

    return render_template(

        "fraud_logs.html",

        fraud_records=fraud_records
    )

# =========================
# BLOCKCHAIN VERIFICATION
# =========================

@app.route("/verify")

def verify_blockchain():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

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

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    data = pd.read_csv(
        "datasets/land_fraud_dataset.csv"
    )

    district_encoder = LabelEncoder()

    land_type_encoder = LabelEncoder()

    verification_encoder = LabelEncoder()

    data["district"] = district_encoder.fit_transform(
        data["district"]
    )

    data["land_type"] = land_type_encoder.fit_transform(
        data["land_type"]
    )

    data["verification_status"] = verification_encoder.fit_transform(
        data["verification_status"]
    )

    X = data[
        [
            "area",
            "transaction_count",
            "market_value",
            "owner_history",
            "transfer_frequency",
            "district",
            "land_type",
            "verification_status"
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
        LogisticRegression(max_iter=1000),

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