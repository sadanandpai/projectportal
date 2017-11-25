if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('./service-worker.js')
    .then(function() { 
      console.log('Trading Masters Service Worker is Registered'); 
    });
}