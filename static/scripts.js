selection = [];

document.addEventListener("DOMContentLoaded", function() {
    cards = document.querySelectorAll(".card")
    for (card of cards) {
        card.addEventListener("click", function(event) {

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
            if (selection.length == 3) {
                
            }
        })
    }
});