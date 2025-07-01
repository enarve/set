selection = [];
if (localStorage.getItem("selection")) {
    selection = JSON.parse(localStorage.getItem("selection"));
}

function saveSelection() {
    localStorage.setItem("selection", JSON.stringify(selection));
}

// function openNavbar() {
//     navbar.classList.remove("show");
//     navbar.setAttribute("aria-expanded", true);
// }

// function closeNavbar() {
//     navbar.classList.add("show");
//     navbar.setAttribute("aria-expanded", false);
// }

function updateAppearance() {
    cards = document.querySelectorAll(".card")
    for (card of cards) {
        if (selection.includes(card.id)) {
            // card.style.backgroundColor = "yellow";
            card.style.borderColor = "rgb(180, 142, 118)";
        } else {
            card.style.borderColor = "";
        }
    }
}

async function fetchCheckState() {
  const url = "/data/check_state";
  try {
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify({ check: true }),
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

    cards = document.querySelectorAll(".card");

    if (selection.length == 3) {
        // Deselect all
        selection = [];
        saveSelection();
    }

    // Change selection
    if (selection.includes(event.target.id)) {
        // Deselect card
        const index = selection.indexOf(event.target.id);
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
                    
                    card.style.borderColor = "green";
                    card.removeEventListener("click", handleCardClick);

                } else {
                    card.style.borderColor = "";
                }
            }
        } else {
            for (card of cards) {
                if (selection.includes(card.id)) {
                    card.style.borderColor = "crimson";
                } else {
                    card.style.borderColor = "";
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

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

document.addEventListener("DOMContentLoaded", async function() {

    result = await fetchCheckState();
    if (result) {
        document.querySelector(".result").innerHTML = "You won!";
        document.querySelector(".deck").style.display = "none";
        
        confetti.setCount(200);
        const times = 10;

        for(let i = 0; i < times; i++){
            document.querySelector("#logo").click();
            sleep(50);
        }
        
 
        alert("Congratulations! You collected all sets!")

    } else {
        document.querySelector(".result").innerHTML = ""
        document.querySelector(".deck").style.display = "";
    }

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