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
    // We gebruiken de ID 'form-per-deelnemer'
    const deelnemerForm = document.getElementById('form-per-deelnemer');

    // Als het formulier gevonden wordt, voeg dan de event listener toe
    if (deelnemerForm) {
        deelnemerForm.addEventListener('submit', function(event) {
            event.preventDefault();

            // Voeg hier de logica toe voor het ophalen en verwerken van de gegevens
            const formData = new FormData(deelnemerForm);
            const data = Object.fromEntries(formData.entries());

            fetch('http://127.0.0.1:8000/api/v1/deelnemer/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => {
                if (!response.ok) {
                    // Als de respons niet OK is, gooi een foutmelding
                    throw new Error('Netwerkrespons was niet ok');
                }
                return response.json();
            })
            .then(responseData => {
                console.log('Succes:', responseData);
                alert('Formulier succesvol verzonden!');
                deelnemerForm.reset(); // Optioneel: reset het formulier
            })
            .catch((error) => {
                console.error('Fout:', error);
                alert('Er is een fout opgetreden bij het verzenden.');
            });
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
            const cursusDatumWaarde = document.getElementById('cursusdatum').value; // Corrected ID
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
            document.getElementById('cursusdatum').value = cursusDatumWaarde; // Corrected ID
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

// Zorg ervoor dat de initDeelnemerForm functie wordt aangeroepen.
initDeelnemerForm();