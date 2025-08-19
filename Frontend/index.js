
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

// Functie om het formulier op de 'Per deelnemer' pagina te initialiseren.
function initDeelnemerForm() {
    // We gebruiken de ID 'deelnemer-form'
    const deelnemerForm = document.getElementById('deelnemer-form');

    // Als het formulier gevonden wordt, voeg dan de event listener toe
    if (deelnemerForm) {
        deelnemerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log('Formulier op de homepagina is ingediend.');
            // Voeg hier de logica toe voor het ophalen en verwerken van de gegevens
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('cursus-deelnemer-formulier');

  if (form) {
    form.addEventListener('submit', function(event) {
      // Voorkom dat de pagina herlaadt
      event.preventDefault();

      // Haal de waarden op van de velden die je wilt behouden
      const cursusTitelWaarde = document.getElementById('cursusTitel').value;
      const cursusDatumWaarde = document.getElementById('cursusDatum').value;
      
      // Verwerk hier je formuliergegevens
      console.log('Formulier verzonden!');
      console.log('Cursus Titel:', cursusTitelWaarde);
      console.log('Cursus Datum:', cursusDatumWaarde);
      
      // Plaats de waarden terug in de velden die je wilt behouden
      document.getElementById('cursusTitel').value = cursusTitelWaarde;
      document.getElementById('cursusDatum').value = cursusDatumWaarde;
      
      // Maak de deelnemersvelden leeg
      document.getElementById('deelnemerNaam').value = '';
      document.getElementById('deelnemerEmail').value = '';
    });
  }
});