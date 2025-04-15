## Endpointtien perustelut

Endpointit on jaettu sensorien (anturi) ja sektorien (lohko) välille. Nimeämiset erikoiset koska halusin tehdä työn englanniksi, enkä keksinyt järkevämpiä käännöksiä. Käytän tässä tekstissä anturin ja lohkon sijaan sensoria ja sektoria luettavuuden vuoksi.

### Sensorit
- `/sensors/`
  - Yksinkertaisesti palauttaa kaikki sensorit.
  - Sisältää query parametrin jolla voi suodattaa sensorit virhetilan mukaan.
  
- `POST /sensors/{sensorId}`
  - Palauttaa yksittäisen sensorin tiedot.
  - Sisältää query parametrit palautettavien mitta-arvojen määrälle ja aikavälille.
  - CRUD-funktion queryissä kesti n. 4 tuntia saada aikaiseksi. Koitin saada ne toteutettua kerralla relationshippien kautta, mutta meni niin vaikeaksi että päädyin tekemään kaksi erillistä queryä ja yhdistämään ne oikeanlaiseksi response modeliksi.

- `PATCH /sensors/{sensorId}`
  - Vaihtaa yksittäisen sensorin vikatilaa. Vaihtaa sen oletukselta päälle, jotta sensorin ei tarvitse lähettää muuta kuin oma tunnisteensa.

- `/sensors/{sensorId}/errorhistory`
  - Palauttaa kaikki yksittäisen sensorin tilamuutokset.

### Sektorit
- `/sectors/{sectorId}`
  - Palauttaa yksittäisen sektorin sensoreineen, ja sen viimeisimmät mittaukset.

## Keinoälyjen käyttö

28.3. Kysytty apua tietokantayhteyden ongelmanratkontaan. Ongelma oli epähuomiossa lisätty `await` avainsana, jota tekoälykään ei huomannut.
29.3. Kysytty apua selvittämään miksi endpoint palauttaa nullia. Ongelma oli `return` avainsanan puuttuminen endpointista. Duh.