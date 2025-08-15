function pingBackend() {
    fetch('http://127.0.0.1:8000/api/v1/ping/')
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        alert('Fout: De backend is niet bereikbaar.');
    });
}