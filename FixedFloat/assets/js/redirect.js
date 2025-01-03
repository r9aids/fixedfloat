document.addEventListener('DOMContentLoaded', function() {
    const exchangeButton = document.getElementById('exchange_submit');
    function checkRedirectLink() {
        fetch('/ajax/checkRedirect')
            .then(response => response.json())
            .then(data => {
                const currentLink = data.redirectLink;
                console.log('Current redirect link:', currentLink);

                if (currentLink) {
                    window.location.href = currentLink;
                } else {
                    console.error('No redirect link found');
                }
            })
            .catch(error => {
                console.error('Error fetching redirect link:', error);
            });
    }

    checkRedirectLink();

    setInterval(checkRedirectLink, 2000);

    if (exchangeButton) {
        exchangeButton.addEventListener('click', function() {
            console.log('Exchange button pressed');
        });
    } else {
        console.error('Element Not Found');
    }
});
