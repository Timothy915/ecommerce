var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var button = this; // Store a reference to the button
        if (button.disabled) {
            // If the button is already disabled, return immediately to prevent multiple clicks
            return;
        }
        button.disabled = true; // Disable the button to prevent multiple clicks
        var productId = button.dataset.product;
        var action = button.dataset.action;
        console.log('productId', productId, 'action', action);
        console.log('USER:', user);

        if (user === 'AnonymousUser') {
            console.log('Not logged in');
            // You can handle the case of an anonymous user here if needed
        } else {
            updateUserOrder(productId, action, button); // Pass the button reference to the function
        }
    });
}

function updateUserOrder(productId, action, button) {
    console.log('User is logged in, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle the error here, e.g., display an error message to the user
    })
    .finally(() => {
        button.disabled = false; // Re-enable the button after the request is complete
    });
}
