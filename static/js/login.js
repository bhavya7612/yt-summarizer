var messageFromFlask = "{{ message }}";

        // Request permission to show notifications
        function requestNotificationPermission() {
            if (Notification.permission === 'granted') {
                showNotification();
            } else if (Notification.permission !== 'denied') {
                Notification.requestPermission().then(permission => {
                    if (permission === 'granted') {
                        showNotification();
                    }
                });
            }
        }

        // Show notification
        function showNotification() {
            new Notification('Flask Notification', {
                body: messageFromFlask,
                icon: 'https://via.placeholder.com/128' // Optional icon for the notification
            });
        }

        // Call the function to request permission and show the notification
        requestNotificationPermission();