selection = [];
if (localStorage.getItem("selection")) {
    selection = JSON.parse(localStorage.getItem("selection"));
}

function saveSelection() {
    localStorage.setItem("selection", JSON.stringify(selection));
}

function updateAppearance() {
    cards = document.querySelectorAll(".card")
    for (card of cards) {
        if (selection.includes(card.id)) {
            card.style.backgroundColor = "yellow";
        } else {
            card.style.backgroundColor = "";
        }
    }
}

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
    return json;
  } catch (error) {
    console.error(error.message);
  }
}

async function fetchUpdate() {
  saveSelection();
  const url = "/";
  try {
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify({ update: true }),
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    return json;
  } catch (error) {
    console.error(error.message);
  }
}

async function handleCardClick(event) {

    cards = document.querySelectorAll(".card")

    if (selection.length == 3) {
        // Deselect all
        selection = [];
        saveSelection()
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
    updateAppearance();

    // Check triple if set
    if (selection.length == 3) {
        result = await fetchCompare();
        if (result) {
            for (card of cards) {
                if (selection.includes(card.id)) {
                    card.style.backgroundColor = "green";
                    card.removeEventListener("click", handleCardClick);
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
    } else {
        result = await fetchUpdate()
        if (result) {
            location.reload()
        }
    }

}

document.addEventListener("DOMContentLoaded", function() {
    updateAppearance();
    cards = document.querySelectorAll(".card")
    for (card of cards) {
        card.addEventListener("click", handleCardClick)
    }

    document.querySelector("#restart").addEventListener("click", function(e) {
        selection = [];
        saveSelection();
    })

    document.querySelector("#deal_more").addEventListener("click", function(e) {
        if (selection.length == 3) {
        // Deselect all
        selection = [];
        }
        saveSelection();
    })
});