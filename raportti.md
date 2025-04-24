## Käännökset

Halusin tehdä työn englanniksi joten käänsin tehtävänannon anturit ja lohkot englanniksi `sector` ja `sensor`. Käytän tässä tekstissä näistä anturin ja lohkon sijaan sanoja sektori ja sensori, luettavuuden vuoksi koodin ja raportin välillä hyppiessä.

## Resurssit

- Sektorit
  - Sisältävät sensoreita.
- Sensorit
  - Sisältävät viittaukset sensorin mittauksiin ja virhehistoriaan.
- Mittaukset (Measurements)
  - Lista mittaustuloksia.


## Tietokantamalleista

Alla on havainnollistava kaavio tietokannan relaatioista:
```
Sector
└── Sensor
    ├── Measurements
    └── ErrorHistory
```

- En kohtele ErrorHistoryä resurssina, mutta sille on silti oma taulunsa joka on vain lista sensorien tilamuutoksia (virhetilaan tai siitä pois).
- Osa endpointtien palauttamista malleista perii `BaseModel`, koska SQLModel ei tue `List`-muotoisia muuttujia joita tarvittiin tietojen palauttamiseen.
- Sensorien mallissa päätin nimetä virhetilan  `hasError` jotta booleanit olisivat helpompia ymmärtää, vrt. "status" jossa truen ja falsen tarkoitus olisi epäselvä.
- Päätin toteuttaa sektorit niin että niitä käpistellään pääasiassa nimen kautta, ei ID-numerolla. Tämä siksi että käyttäjän on mahdollista nimetä niitä alfanumeerisesti, eikä rajattuna pelkästään numeroihin. ID löytyy kyllä primary keynä tietokannasta relaatioita varten, ja se palautuu kaikki sektorit listatessa.

## Endpointeista

Jätin työmäärän vähentämiseksi tietoisesti joitain endpointteja tekemättä jotka todennäköisesti oikeassa järjestelmässä olisivat, mutta joille ei oltu määritelty tehtävänannossa tarvetta. Esim. sektorien/sensorien uudelleennimeäminen/poistaminen, tai sensorien siirtäminen sektorista toiseen.

### Sensorit

- `/sensors/`
  - Palauttaa kaikki sensorit.
  - Sisältää query parametrin jolla voi suodattaa sensorit virhetilan mukaan.

- `/sensors/new`
  - Luo uuden sensorin.
  - Luo automaattisesti uuden sektorin, jos nimettyä ei ole olemassa.

- `/sensors/errors`
  - Palauttaa listan kaikista virhetapahtumista. Sisältää tiedot jotka voi frontin puolella käsitellä graafiksi, tai vaikka muuntaa CSV-muotoon ja antaa käyttäjälle.
  
- `GET /sensors/{sensorId}`
  - Palauttaa yksittäisen sensorin tiedot.
  - Sisältää query parametrit palautettavien mittausten määrälle ja aikavälille.
  - CRUD-funktion queryissä kesti n. 4 tuntia saada aikaiseksi. Koitin saada ne toteutettua kerralla relationshippien kautta, mutta meni niin vaikeaksi että päädyin tekemään kaksi erillistä queryä ja yhdistämään ne oikeanlaiseksi response modeliksi.

- `PATCH /sensors/{sensorId}`
  - Vaihtaa yksittäisen sensorin vikatilaa. Vaihtaa sen oletukselta päälle, jotta sensorin ei tarvitse lähettää muuta kuin oma tunnisteensa.
  - Palauttaa luodun ErrorHistory-objektin, lähinnä fronttia varten jos sensori vaihdetaan manuaalisesti pois vikatilasta.

- `/sensors/{sensorId}/errors`
  - Sama kuin `/sensors/errors` mutta rajattuna vain tiettyyn sensoriin.


### Mittaukset

- `/measurement`
  - Kirjaa uuden lämpötilamittauksen.

### Sektorit

- `GET /sectors`
  - Palauttaa listan kaikista sektoreista.

- `POST /sectors`
  - Luo uuden sektorin. 

- `/sectors/{sectorName}`
  - Palauttaa yksittäisen sektorin sensoreineen, ja jokaisen viimeisimmät mittaukset.

## Keinoälyjen käyttö

28.3. Kysytty apua tietokantayhteyden ongelmanratkontaan. Ongelma oli epähuomiossa lisätty `await` avainsana, jota tekoälykään ei huomannut ongelmaksi.
29.3. Kysytty apua selvittämään miksi endpoint palauttaa nullia. Ongelma oli `return` avainsanan puuttuminen endpointista. Duh.