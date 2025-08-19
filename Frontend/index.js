
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
  const form = document.getElementById('form-per-cursus');
  const dropdown = document.getElementById('geldigheid-jaren');
  const datumInput = document.getElementById('geldigheid-datum-input');

  if (form) {
    form.addEventListener('submit', function(event) {
      // Voorkom dat de pagina herlaadt
      event.preventDefault();

      // Haal de waarden op van de velden die je wilt behouden
      const cursusWaarde = document.getElementById('cursus').value;
      const cursusDatumWaarde = document.getElementById('cursusDatum').value;
      const isRefresherChecked = document.getElementById('refresherCheck').checked;
      const geldigheidWaarde = document.getElementById('geldigheid-jaren').value;
      const aangepasteDatumWaarde = document.getElementById('geldigheid-datum-input').value;
      
      // Verwerk hier je formuliergegevens
      console.log('Formulier verzonden!');
      console.log('Cursus:', cursusWaarde);
      console.log('Cursus Datum:', cursusDatumWaarde);
      console.log('Is de refresher aangevinkt?', isRefresherChecked);
      console.log('Geldigheid:', geldigheidWaarde);
      console.log('Aangepaste datum:', aangepasteDatumWaarde);
      
      // Plaats de waarden terug in de velden die je wilt behouden
      document.getElementById('cursus').value = cursusWaarde;
      document.getElementById('cursusDatum').value = cursusDatumWaarde;
      document.getElementById('refresherCheck').checked = isRefresherChecked;
      document.getElementById('geldigheid-jaren').value = geldigheidWaarde;
      document.getElementById('geldigheid-datum-input').value = aangepasteDatumWaarde;

      // Maak de deelnemersvelden leeg
      document.getElementById('voornaam').value = '';
      document.getElementById('tussenvoegsel').value = '';
      document.getElementById('achternaam').value = '';
      document.getElementById('bedrijfsnaam').value = '';
      document.getElementById('email').value = '';
      document.getElementById('geboortedatum').value = '';
      document.getElementById('windaId').value = '';
    });
  }

  if (dropdown && datumInput) {
    dropdown.addEventListener('change', function() {
      if (this.value === 'custom') {
        datumInput.hidden = false;
      } else {
        datumInput.hidden = true;
      }
    });
  }
});