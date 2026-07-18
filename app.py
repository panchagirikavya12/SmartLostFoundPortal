from flask import Flask, render_template, request
from db import cursor, db

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/report-lost", methods=["GET", "POST"])
def report_lost():
    if request.method == "POST":
        item_name = request.form["item_name"]
        category = request.form["category"]
        location = request.form["location"]
        date = request.form["date"]
        description = request.form["description"]

        sql = """
            INSERT INTO lost_items
            (item_name, category, location, lost_date, description)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (item_name, category, location, date, description)

        cursor.execute(sql, values)
        db.commit()

        return render_template("success.html")

    return render_template("report_lost.html")


@app.route("/report-found", methods=["GET", "POST"])
def report_found():
    if request.method == "POST":
        item_name = request.form["item_name"]
        category = request.form["category"]
        location = request.form["location"]
        date = request.form["date"]
        description = request.form["description"]

        sql = """
            INSERT INTO found_items
            (item_name, category, location, found_date, description)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (item_name, category, location, date, description)

        cursor.execute(sql, values)
        db.commit()

        return render_template("success.html")

    return render_template("report_found.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_term = request.form["search"]

        cursor.execute(
            """
            SELECT item_name, category, location, lost_date
            FROM lost_items
            WHERE item_name LIKE %s
            """,
            ("%" + search_term + "%",),
        )
        lost_items = cursor.fetchall()

        cursor.execute(
            """
            SELECT item_name, category, location, found_date
            FROM found_items
            WHERE item_name LIKE %s
            """,
            ("%" + search_term + "%",),
        )
        found_items = cursor.fetchall()
    else:
        cursor.execute(
            "SELECT item_name, category, location, lost_date FROM lost_items"
        )
        lost_items = cursor.fetchall()

        cursor.execute(
            "SELECT item_name, category, location, found_date FROM found_items"
        )
        found_items = cursor.fetchall()

    return render_template(
        "search.html",
        lost_items=lost_items,
        found_items=found_items,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password),
        )
        user = cursor.fetchone()

        if user:
            return render_template("login_success.html")

        return render_template("login_failed.html")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        sql = """
            INSERT INTO users(fullname, email, phone, password)
            VALUES (%s, %s, %s, %s)
        """
        values = (fullname, email, phone, password)

        cursor.execute(sql, values)
        db.commit()

        return render_template("success.html")

    return render_template("register.html")


@app.route("/admin")
def admin():
    cursor.execute(
        "SELECT item_name, category, location, lost_date FROM lost_items"
    )
    lost_items = cursor.fetchall()

    cursor.execute(
        "SELECT item_name, category, location, found_date FROM found_items"
    )
    found_items = cursor.fetchall()

    return render_template(
        "admin.html",
        lost_items=lost_items,
        found_items=found_items,
    )


if __name__ == "__main__":
    app.run(debug=True)