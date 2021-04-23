# reseptiSovellus

Sovelluksessa löytyy lista ruokaresepteistä, joita klikkaamalla ne pääsee näkemään.
Sovelluksessa on kirjautuminen ja peruskäyttäjiä tai pääkäyttäjiä.
Kaikki käyttäjät voivat luoda omia reseptilistoja sovelluksesta löytyvien reseptien pohjalta.
Osa sivun ominaisuuksista on saatavilla vain reseptin luojalle sekä pääkäyttäjille.

### Projektin tämän hetkinen tila

* Etusivulla kirjautuminen ja tunnuksen luominen, missä linkit muihin näkymiin kirjautumisen jälkeen
* Kaikkien reseptien näkymä missä kaikki reseptit listana
* Kaikkien reseptien järjestys sen mukaan monta kertaa lisätty käyttäjälistalle eli reseptin suosio
* Sivu reseptin luomista varten
* Reseptin oma näkymä kun sitä klikkaa, mitkä ainekset sekä muita reseptiin liittyviä tietoja, kaikki käyttäjät voivat kommentoida reseptejä
* Kaikki käyttäjät voivat lisätä ja poistaa reseptejä omalla henkilökohtaisella listalla
* Pääkäyttäjällä käytettävissä kaikki ominaisuudet
* Reseptin luoja voi poistaa ja muokata reseptejä sekä poistaa reseptin kommentteja
* Kommentin kirjoittaja voi muokata ja poistaa omat kommenttinsa
* Sivu on suojattu kurssimateriaalin esimerkkien mukaan esim. CSRF hyökkäystä vastaan.

sovellusta voi testata osoitteessa:
https://tsoha-resepteja.herokuapp.com/

Tietokannasta löytyy valmiiksi tunnus pääkäyttäjän oikeuksilla
tunnus: Admintunnus
sekä salasana: Admintunnus


### TODO

Ohjaajalta kaipaisin ehkä neuvoa kannattaako lähteä laajentamaan vielä vai onko työ jo ihan kelpo kooltaan kun on vain 6 tietokantataulua.

### Tietokantakaavio

![RunTimes](https://github.com/synesteesia/reseptiSovellus/blob/main/Tietokantakaavio/kaavio1.jpg)


### Laajennusideoita kurssin jälkeen

* Käyttäjä voi luoda kauppalista pohjia.
* Käyttäjä voi valita reseptejä ja lisätä niiden ainekset kauppalistaan.
* Käyttäjä voi poistaa, lisätä ja muokata aineksia kauppalistassa.
* Käyttäjä voi luoda jääkaapissa listan, mihin voi lisätä kauppalistan sisällön ja poistaa entisten kauppalistojen sisältöjä tai yksittäisiä aineksia
* Jos jääkaapissa listassa on jo jokin aines, uuteen kauppalistaan tulee siitä ilmoitusmerkki


