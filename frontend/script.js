const form = document.getElementById("roomForm");

const teamNameInput = document.getElementById("teamName");

const assignButton = document.getElementById("assignButton");

const errorMessage = document.getElementById("errorMessage");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const teamName = teamNameInput.value.trim();

    errorMessage.textContent = "";

    if (!teamName) {
        errorMessage.textContent = "Please enter your team name.";
        return;
    }


    assignButton.disabled = true;

    assignButton.textContent = "Assigning...";


    try {

        const response = await fetch("/api/assign", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                team_name: teamName
            })

        });


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message || "Unable to assign room."
            );

        }


        // Save the assignment locally.
        localStorage.setItem(
            "assignedTeam",
            data.team_name
        );

        localStorage.setItem(
            "assignedRoom",
            data.room
        );


        // Go to result page
        window.location.href =
            `/result.html?team=${encodeURIComponent(data.team_name)}&room=${data.room}`;


    } catch (error) {

        console.error(error);

        errorMessage.textContent =
            error.message ||
            "Something went wrong. Please try again.";

        assignButton.disabled = false;

        assignButton.textContent = "Assign My Room";

    }

});