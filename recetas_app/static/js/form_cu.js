const date_made = document.querySelector('#made_on');

(function() {
    const today = new Date().toISOString().split('T')[0];
    date_made.setAttribute('max', today);
})();