function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const items = document.getElementsByClassName('rating-item');
for (let item of items) {
    const [upvote_btn, counter, downvote_btn] = item.children;
    upvote_btn.addEventListener('click', () => {
        const formData = new FormData();

        formData.append('id', item.dataset.id)
        formData.append('rating', 'u')

        const request = new Request('/question_like/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log({ data });
                counter.innerHTML = data.rating;
            });
    });

    downvote_btn.addEventListener('click', () => {
        const formData = new FormData();

        formData.append('id', item.dataset.id)
        formData.append('rating', 'd')

        const request = new Request('/question_like/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log({ data });
                counter.innerHTML = data.rating;
            });
    })
}