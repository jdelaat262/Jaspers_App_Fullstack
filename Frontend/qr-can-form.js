// Wacht tot de DOM volledig geladen is voordat scripts worden uitgevoerd
document.addEventListener('DOMContentLoaded', () => {
    // Referentie naar het formulier
    const qrScanForm = document.getElementById('qr-scan-form');

    // Functie om URL-parameters te parsen
    const getUrlParams = () => {
        const params = {};
        // Maak een URLSearchParams object van de huidige URL's query string
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        
        // Loop over alle parameters en sla ze op in het params object
        for (const [key, value] of urlParams.entries()) {
            params[key] = value;
        }
        return params;
    };

    // Haal de parameters op uit de URL
    const params = getUrlParams();

    // Vul de formuliervelden met de ontvangen parameters
    // Certificaat gegevens
    if (params.cursusNaam) {
        document.getElementById('scannedCursusNaam').value = decodeURIComponent(params.cursusNaam);
    }
    if (params.cursusdatum) {
        document.getElementById('scannedCursusdatum').value = decodeURIComponent(params.cursusdatum);
    }
    if (params.geldigheidJaren) {
        document.getElementById('scannedGeldigheid').value = decodeURIComponent(params.geldigheidJaren) + ' jaar';
    }
    if (params.refresher === 'true') {
        document.getElementById('scannedRefresher').checked = true;
    }

    // Event listener voor het versturen van het formulier
    qrScanForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Voorkom standaard formulierinzending

        // Verzamel alle gegevens van het formulier
        const formData = {
            cursusNaam: document.getElementById('scannedCursusNaam').value,
            cursusdatum: document.getElementById('scannedCursusdatum').value,
            geldigheidJaren: document.getElementById('scannedGeldigheid').value.replace(' jaar', ''), // Verwijder ' jaar' voor opslag
            refresher: document.getElementById('scannedRefresher').checked,
            aanhef: document.querySelector('input[name="aanhef"]:checked')?.value || '',
            voornaam: document.getElementById('voornaam').value,
            tussenvoegsel: document.getElementById('tussenvoegsel').value,
            achternaam: document.getElementById('achternaam').value,
            bedrijfsnaam: document.getElementById('bedrijfsnaam').value,
            email: document.getElementById('email').value,
            geboortedatum: document.getElementById('geboortedatum').value,
            windaId: document.getElementById('windaId').value,
            telefoonnummer: document.getElementById('telefoonnummer').value
        };

        console.log('Gegevens om te versturen:', formData);

        // TODO: Hier komt de logica om de gegevens naar je database te sturen.
        // Dit is een placeholder. Je zou hier een fetch-request kunnen doen naar een backend API.
        try {
            // Voorbeeld van een fetch-request naar een fictieve API:
            // const response = await fetch('/api/certificaten-registratie', {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //     },
            //     body: JSON.stringify(formData),
            // });

            // const result = await response.json();

            // Als de database-operatie succesvol is:
            // console.log('Registratie succesvol:', result);
            alert('Certificaat succesvol geregistreerd! (Simulatie - gegevens niet echt opgeslagen)');
            
            // Je kunt hier de gebruiker doorverwijzen of een succesbericht tonen
            // window.location.href = 'succes.html';

        } catch (error) {
            console.error('Fout bij het versturen van gegevens:', error);
            alert('Er is een fout opgetreden bij de registratie. Probeer het opnieuw.');
        }
    });
});
