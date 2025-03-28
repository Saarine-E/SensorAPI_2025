## Endpointtien perustelut

Endpointit on jaettu anturien (sensor) ja lohkojen (section) välille.

### Anturit
- `/sensors/`
  - Yksinkertaisesti palauttaa kaikki anturit.
  - Sisältää query parametrin jolla voi suodattaa palautettavat anturit virhetilan mukaan.
- `/sensors/{sensorId}`
  - Palauttaa yksittäisen anturin tiedot.
  - Sisältää query parametrin palautettavien mitta-arvojen määrälle.
- `/sensors/{sensorId}/statehistory`
  - Palauttaa kaikki yksittäisen anturin tilamuutokset. Loogisesti laajennus ylläolevaan, koska tilamuutokset koskevat aina yksittäistä anturia.

## Keinoälyjen käyttö

28.3. Kysytty apua tietokantayhteyden ongelman ratkontaan (ongelma oli epähuomiossa lisätty `await` avainsana)