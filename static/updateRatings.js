const editButtons = document.querySelectorAll('.edit-movie-rating');

for (const button of editButtons) {
    button.addEventListener('click', () => {

        const newScore = prompt("What is your new rating?");
        const ratingID = button.id;
        const formInputs = {
            "rating_id": ratingID,
            "updated_score": newScore,
        }

        fetch('/update_rating', {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.text())
        .then((responseText) => {
            const scoreHTML = document.querySelector();
            scoreHTML.innerHTML = newScore;
        })

    })
}