# reseptiSovellus

Sovelluksessa löytyy lista ruokaresepteistä, joita klikkaamalla ne pääsee näkemään.
Sovelluksessa on kirjautuminen ja peruskäyttäjiä tai pääkäyttäjiä.
Kaikki käyttäjät voivat luoda omia reseptilistoja sovelluksesta löytyvien reseptien pohjalta.
Osa sivun ominaisuuksista on saatavilla vain reseptin luojalle sekä pääkäyttäjille.

### Projektin tämän hetkinen tila

* Etusivulla kirjautuminen ja tunnuksen luominen, missä linkit muihin näkymiin kirjautumisen jälkeen
* Sivu reseptin luomista varten
* Kaikkien reseptien näkymä missä kaikki reseptit listana
* Reseptin oma näkymä kun sitä klikkaa, mitkä ainekset sekä muita reseptiin liittyviä tietoja, kaikki käyttäjät voivat kommentoida reseptejä
* Kaikki käyttäjät voivat lisätä reseptejä omalle henkilökohtaiselle listalle
* Kaikkien reseptien järjestys sen mukaan monta kertaa lisätty käyttäjälistalle eli reseptin suosio
* Osa sivuston ominaisuuksista vain pääkäyttäjän ja reseptin tekijän käytettäissä
* Sivu on suojattu kurssimateriaalin esimerkkien mukaan esim. CSRF hyökkäystä vastaan.

sovellusta voi testata osoitteessa:
https://tsoha-resepteja.herokuapp.com/

Tietokannasta löytyy valmiiksi tunns
tunnus: testitunnus
sekä salasana: testitunnus


### TODO

Sovellusta ei ole juurikaan purettu vielä erillisiin komponentteihin, esimerkiksi routet ovat kaikki vielä samassa tiedostossa.


### Laajennusideoita kurssin jälkeen

* Käyttäjä voi valita reseptejä ja lisätä niiden ainekset kauppalistaan.
* Käyttäjä voi luoda jääkaapissa listan, mihin voi lisätä kauppalistan sisällön ja poistaa entisten kauppalistojen sisältöjä tai yksittäisiä aineksia
* Jos jääkaapissa listassa on jo jokin aines, uuteen kauppalistaan tulee siitä ilmoitusmerkki


