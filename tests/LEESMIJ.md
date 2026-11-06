# Jurycoach – ByteTrack versus BoT-SORT met ReID

Deze proef vergelijkt de **twee trackers met dezelfde YOLO-persoonsdetector**. De videobeelden blijven op je eigen computer; upload ze niet naar een openbare GitHub-repository.

1. Installeer Python 3.11 of 3.12 voor Windows.
2. Download de bestanden `vergelijk_trackers.py` en `start_windows.bat` uit deze map, en leg ze samen in een nieuwe map op je computer. Zet ook `Js 9-9.mp4` en optioneel `VTV_Acro_Trainingsanalyse_v126.json` in dezelfde map.
3. Open `start_windows.bat`. Er worden Python-pakketten en modelgewichten op je eigen computer gedownload; zonder GPU kan de verwerking lang duren. Er is een internetverbinding nodig voor de eerste installatie.
4. Op het stilstaande beeld rond 00:50 klik je **gymnast 1** en **gymnast 2** bij de romp aan. Druk Enter; R maakt de keuze leeg.
5. De twee trackers starten ieder met **dezelfde twee aanklikpunten**, hetzelfde persoonsdetectiemodel, hetzelfde videofragment vanaf 00:50 en dezelfde analysefrequentie (5 fps).
6. Kijk in `tracker-resultaten`. Je krijgt `ByteTrack_metingen.csv`, `BoT-SORT_ReID_metingen.csv`, `vergelijking.json` en (lokaal) voorbeeldbeelden. Laad de twee CSV's in [de vergelijking binnen Jurycoach](../tracking-test.html).

**Niet verwarren:** ‘beide geselecteerde track-ID's aanwezig’ betekent NIET dat zeker de juiste twee gymnasten worden gevolgd. Controleer beide personen na overlap en eventuele trainerverwarring zelf. Daarom bevatten de CSV's aparte controlekolommen voor: `controle_echt_dezelfde_2`, `trainer_ten_onrechte_gevolgd`, `persoonswisseling`.

Deze proef is voorlopig **geen geïntegreerde tracker in de website**. Een GitHub Pages-site kan niet zomaar een lokaal Python-model draaien. De berekening gebeurt op je eigen computer; de website vergelijkt de resultaten. De eerdere Jurycoach v126-analyse gebruikte het volledige beeld en een ander posemodel, waardoor die niet als gelijkwaardige YOLO-baseline telt.

De modelkeuze volgt de [officiële Ultralytics trackingdocumentatie](https://docs.ultralytics.com/modes/track/). In de test wordt `botsort.yaml` gekopieerd met `with_reid: true`. Die parameter kan extra modellen downloaden. Als ReID ontbreekt of faalt, rapporteert de proef dat als fout, niet als geslaagde ReID-test. Controleer vóór commerciële verspreiding de licenties van de gebruikte software en modellen. 
