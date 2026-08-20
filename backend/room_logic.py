import random
import sqlite3

ROOMS = [1, 2, 3, 4]


def normalize_team_name(team_name):
    return " ".join(team_name.strip().split()).lower()


def get_room_counts(conn):
    counts = {
        room: 0
        for room in ROOMS
    }

    rows = conn.execute("""
        SELECT room_number, COUNT(*) AS count
        FROM teams
        GROUP BY room_number
    """).fetchall()

    for row in rows:
        room = row["room_number"]

        if room in counts:
            counts[room] = row["count"]

    return counts


def assign_room(conn, team_name):

    team_name = " ".join(team_name.strip().split())

    if not team_name:
        raise ValueError("Team name cannot be empty.")

    normalized_name = normalize_team_name(team_name)

    # Start an immediate transaction.
    # This helps prevent two people from getting
    # assigned based on the same room counts.
    conn.execute("BEGIN IMMEDIATE")

    try:

        # Check if this team already exists.
        existing_team = conn.execute("""
            SELECT id, team_name, room_number
            FROM teams
            WHERE LOWER(TRIM(team_name)) = ?
        """, (normalized_name,)).fetchone()

        if existing_team:
            conn.commit()

            return {
                "success": True,
                "already_assigned": True,
                "team_name": existing_team["team_name"],
                "room": existing_team["room_number"]
            }

        # Get current room distribution
        counts = get_room_counts(conn)

        minimum_count = min(counts.values())

        # Only choose from rooms having the minimum count
        available_rooms = [
            room
            for room, count in counts.items()
            if count == minimum_count
        ]

        # Randomly select one of the least-filled rooms
        selected_room = random.choice(available_rooms)

        # Save assignment
        conn.execute("""
            INSERT INTO teams (team_name, room_number)
            VALUES (?, ?)
        """, (team_name, selected_room))

        conn.commit()

        return {
            "success": True,
            "already_assigned": False,
            "team_name": team_name,
            "room": selected_room
        }

    except sqlite3.IntegrityError:

        conn.rollback()

        # In the unlikely case another request inserted
        # the same team at almost exactly the same time,
        # retrieve the existing assignment.

        existing_team = conn.execute("""
            SELECT team_name, room_number
            FROM teams
            WHERE LOWER(TRIM(team_name)) = ?
        """, (normalized_name,)).fetchone()

        if existing_team:
            return {
                "success": True,
                "already_assigned": True,
                "team_name": existing_team["team_name"],
                "room": existing_team["room_number"]
            }

        raise

    except Exception:
        conn.rollback()
        raise