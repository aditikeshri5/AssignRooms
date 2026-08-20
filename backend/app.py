from flask import Flask, request, jsonify, send_from_directory
from database import init_db, get_db
from room_logic import assign_room, get_room_counts, ROOMS
import os


app = Flask(__name__)

# Initialize database
init_db()


# --------------------------------------------------
# FRONTEND
# --------------------------------------------------

FRONTEND_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "frontend"
    )
)


@app.route("/")
def home():
    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(
        FRONTEND_DIR,
        filename
    )


# --------------------------------------------------
# ASSIGN ROOM
# --------------------------------------------------

@app.route("/api/assign", methods=["POST"])
def assign():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received."
        }), 400

    team_name = data.get("team_name", "").strip()

    if not team_name:
        return jsonify({
            "success": False,
            "message": "Please enter a team name."
        }), 400

    if len(team_name) > 100:
        return jsonify({
            "success": False,
            "message": "Team name is too long."
        }), 400

    try:

        with get_db() as conn:

            result = assign_room(
                conn,
                team_name
            )

        return jsonify(result)

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Something went wrong. Please try again."
        }), 500


# --------------------------------------------------
# ROOM STATUS
# --------------------------------------------------

@app.route("/api/status", methods=["GET"])
def status():

    try:

        with get_db() as conn:

            counts = get_room_counts(conn)

            teams = conn.execute("""
                SELECT team_name, room_number, created_at
                FROM teams
                ORDER BY created_at ASC
            """).fetchall()

        team_list = []

        for team in teams:
            team_list.append({
                "team_name": team["team_name"],
                "room": team["room_number"],
                "created_at": team["created_at"]
            })

        return jsonify({
            "success": True,
            "rooms": counts,
            "total": sum(counts.values()),
            "teams": team_list
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Could not load status."
        }), 500


# --------------------------------------------------
# RESET
# --------------------------------------------------

@app.route("/api/reset", methods=["POST"])
def reset():

    try:

        with get_db() as conn:

            conn.execute("DELETE FROM teams")
            conn.commit()

        return jsonify({
            "success": True,
            "message": "All assignments have been reset."
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Could not reset assignments."
        }), 500


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )