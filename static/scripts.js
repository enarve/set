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
  } catch (error) {
    console.error(error.message);
  }
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
            if (selection.includes(event.target)) {
                // Deselect card
                const index = selection.indexOf(event.target)
                if (index > -1) {
                    selection.splice(index, 1);
                }
            } else {
                // Select card
                selection.push(event.target);
            }

            // console.log(event.target)

            // Update appearance
            
            for (card of cards) {
                if (selection.includes(card)) {
                    card.style.backgroundColor = "yellow";
                } else {
                    card.style.backgroundColor = "";
                }
            }

            // Check triple if set
            console.log(selection);
            if (selection.length == 3) {
                await fetchCompare();
            }
        })
    }
});