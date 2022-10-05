importScripts('https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js')
importScripts('https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js')

const firebaseConfig = {
    apiKey: "AIzaSyAYA_vrqh0lZwYddKCmpz3wtjxHAzklymw",
    authDomain: "mystudentmanagementsystem.firebaseapp.com",
    projectId: "mystudentmanagementsystem",
    storageBucket: "mystudentmanagementsystem.appspot.com",
    messagingSenderId: "387678679441",
    appId: "1:387678679441:web:73496e301d0e7f533b2a30",
    measurementId: "G-Y8RXSLPSQZ"
};

fireabse.initializeApp({
    'messagingSenderID': '387678679441',
})

const messaging = firebase.messaging()
messaging.setBackgroundMessagingHandler(function (payload) {
    console.log(payload);
    const notification = JSON.parse(payload)
    const notificationOption = {
        body: notification.body,
        icon: notification.icon
    }
    return self.ServiceWorkerRegistration.showNotification(payload.notification.title, notificationOption)
})