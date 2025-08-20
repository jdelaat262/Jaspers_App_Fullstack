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

 // Selecteer het formulier voor 'Per cursus'
    const cursusForm = document.getElementById('form-per-cursus');
    if (cursusForm) {
        cursusForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const submitButton = cursusForm.querySelector('button[type="submit"]');
            if (submitButton) submitButton.disabled = true;

            const formData = new FormData(cursusForm);
            const data = Object.fromEntries(formData.entries());
            
            // De correcte logica om de refresher-waarde te verwerken
            const refresherValue = !!data.refreshercheck;
            delete data.refreshercheck;
            data.refresher = refresherValue;
            
            // Controleer of er een aanhef is geselecteerd. Anders, maak het een lege string of null.
            data.aanhef = data.aanhef || ''; 

            if (data.geboortedatum === '') {
                data.geboortedatum = null;
            }
            if (data.cursusdatum === '') {
                data.cursusdatum = null;
            }
            if (data.geldigheid_datum === '') {
                data.geldigheid_datum = null;
            }
            
            if (data['geldigheid-jaren'] === 'custom' && data['geldigheid-datum-input']) {
                 data.geldigheid = data['geldigheid-datum-input'];
            } else {
                 data.geldigheid = data['geldigheid-jaren'];
            }
            // Verwijder de tijdelijke velden
            delete data['geldigheid-jaren'];
            delete data['geldigheid-datum-input'];

            // Beide formulieren sturen nu de data naar dezelfde API
            fetch('http://127.0.0.1:8000/api/v1/cursus_deelnemer/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
                })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Netwerkrespons was niet ok');
                }
                return response.json();
            })
            .then(responseData => {
                console.log('Succes:', responseData);
                alert('Formulier succesvol verzonden!');
                
                document.getElementById('cursus').value = data.cursus;
                document.getElementById('cursusdatum').value = data.cursusdatum;
                document.getElementById('refresherCheck').checked = data.refresher;
                document.getElementById('geldigheid-jaren').value = data.geldigheid;

                document.getElementById('voornaam').value = '';
                document.getElementById('tussenvoegsel').value = '';
                document.getElementById('achternaam').value = '';
                document.getElementById('bedrijfsnaam').value = '';
                document.getElementById('email').value = '';
                document.getElementById('geboortedatum').value = '';
                document.getElementById('windaId').value = '';
            })
            .catch((error) => {
                console.error('Fout:', error);
                alert('Er is een fout opgetreden bij het verzenden.');
            })
            .finally(() => {
                if (submitButton) submitButton.disabled = false;
            });
        });
    }

    const dropdown = document.getElementById('geldigheid-jaren');
    const datumInput = document.getElementById('geldigheid-datum-input');
    if (dropdown && datumInput) {
        dropdown.addEventListener('change', function() {
            if (this.value === 'custom') {
                datumInput.hidden = false;
            } else {
                datumInput.hidden = true;
            }
        });
    }