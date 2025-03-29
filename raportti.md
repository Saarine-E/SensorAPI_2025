## Endpointtien perustelut

Endpointit on jaettu sensorien (anturi) ja sektorien (lohko) välille. Nimeämiset erikoiset koska halusin tehdä työn englanniksi, enkä keksinyt järkevämpiä käännöksiä. Käytän tässä tekstissä anturin ja lohkon sijaan sensoria ja sektoria luettavuuden vuoksi.

### Sensorit
- `/sensors/`
  - Yksinkertaisesti palauttaa kaikki sensorit.
  - Sisältää query parametrin jolla voi suodattaa palautettavat sensorit virhetilan mukaan.
  
- `/sensors/{sensorId}`
  - Palauttaa yksittäisen sensorin tiedot.
  - Sisältää query parametrit palautettavien mitta-arvojen määrälle ja aikavälille.
  - CRUD-funktion queryissä kesti n. 4 tuntia saada aikaiseksi. Koitin saada ne toteutettua kerralla relationshippien kautta, mutta meni niin vaikeaksi että päädyin tekemään kaksi erillistä selectiä ja yhdistämään ne oikeanlaiseksi response modeliksi.

- `/sensors/{sensorId}/errorhistory`
  - Palauttaa kaikki yksittäisen sensorin tilamuutokset. Loogisesti laajennus ylläolevaan, koska tilamuutokset koskevat aina yksittäistä sensoria.

### Sektorit
- `/sectors/{sectorId}`
  - Palauttaa yksittäisen sektorin sensoreineen, ja näiden viimeisimmät mittaukset.

## Keinoälyjen käyttö

28.3. Kysytty apua tietokantayhteyden ongelmanratkontaan. Ongelma oli epähuomiossa lisätty `await` avainsana, jota tekoälykään ei huomannut.
29.3. Kysytty apua selvittämään miksi endpoint palauttaa nullia. Ongelma oli `return` avainsanan puuttuminen endpointista. Duh.