async function loadStatus() {

    try {

        const response =
            await fetch("/api/status");

        const data =
            await response.json();


        if (!data.success) {
            throw new Error(data.message);
        }


        document.getElementById("total")
            .textContent =
            `Total Teams: ${data.total}`;


        const roomsContainer =
            document.getElementById("rooms");


        roomsContainer.innerHTML = "";


        for (let room = 1; room <= 4; room++) {

            const count =
                data.rooms[room] || 0;


            const card =
                document.createElement("div");

            card.className = "room-card";


            card.innerHTML = `
                <div class="room-name">
                    Room ${room}
                </div>

                <div class="room-count">
                    ${count}
                </div>

                <div>
                    Teams
                </div>
            `;


            roomsContainer.appendChild(card);
        }


        const table =
            document.getElementById("teamTable");


        table.innerHTML = "";


        data.teams.forEach(team => {

            const row =
                document.createElement("tr");


            row.innerHTML = `
                <td>${team.team_name}</td>
                <td>Room ${team.room}</td>
                <td>${team.created_at}</td>
            `;


            table.appendChild(row);

        });


    } catch (error) {

        console.error(error);

        alert(
            "Could not load room status."
        );

    }

}


document
    .getElementById("resetButton")
    .addEventListener(
        "click",
        async function () {

            const confirmed =
                confirm(
                    "Are you sure you want to reset ALL assignments?"
                );


            if (!confirmed) {
                return;
            }


            try {

                const response =
                    await fetch(
                        "/api/reset",
                        {
                            method: "POST"
                        }
                    );


                const data =
                    await response.json();


                if (!data.success) {
                    throw new Error(data.message);
                }


                alert(
                    "All assignments have been reset."
                );


                loadStatus();


            } catch (error) {

                console.error(error);

                alert(
                    "Could not reset assignments."
                );

            }

        }
    );


loadStatus();


// Automatically refresh every 5 seconds
setInterval(
    loadStatus,
    5000
);