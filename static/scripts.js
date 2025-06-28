selection = [];

async function fetchCompare() {
  const url = "/data/compare";
  try {
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify({ selection: selection }),
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    console.log(json);
    return json;
  } catch (error) {
    console.error(error.message);
  }
//   return;
}

document.addEventListener("DOMContentLoaded", function() {
    cards = document.querySelectorAll(".card")
    for (card of cards) {
        card.addEventListener("click", async function(event) {

            if (selection.length == 3) {
                // Deselect all
                selection = [];
            }

            // Change selection
            if (selection.includes(event.target.id)) {
                // Deselect card
                const index = selection.indexOf(event.target.id)
                if (index > -1) {
                    selection.splice(index, 1);
                }
            } else {
                // Select card
                selection.push(event.target.id);
            }

            // Update appearance
            for (card of cards) {
                if (selection.includes(card.id)) {
                    card.style.backgroundColor = "yellow";
                } else {
                    card.style.backgroundColor = "";
                }
            }

            // Check triple if set
            if (selection.length == 3) {
                result = await fetchCompare();
                if (result) {
                    for (card of cards) {
                        if (selection.includes(card.id)) {
                            card.style.backgroundColor = "green";
                        } else {
                            card.style.backgroundColor = "";
                        }
                    }
                } else {
                    for (card of cards) {
                        if (selection.includes(card.id)) {
                            card.style.backgroundColor = "red";
                        } else {
                            card.style.backgroundColor = "";
                        }
                    }
                }
            }
        })
    }
});