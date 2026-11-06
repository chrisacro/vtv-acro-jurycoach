# VTV Acro Jurycoach — vergelijking wedstrijdblad en keuze computer-visionmodel

Datum: 6 november 2026  
Casus: `Js 9-9.mp4` — duo, Supplement 3 senior, 149,93 seconden.  
Referentie: `Sup 3 duo.pdf` (Acro Companion wedstrijdkaart) en de door de trainer beoordeelde exports `VTV_Acro_Trainingsanalyse_v124 (1).json` en `VTV_Acro_Trainingsanalyse_v126.json`.

## Status en methodische beperking

Het originele videobestand is 403.728.954 bytes, groter dan de downloadlimiet van 268.435.456 bytes van de beschikbare Drive-koppeling. Daarom is dit **een brongetrouwe vergelijking van wedstrijdkaart, AI-controlebeelden en menselijke reviewlabels** en **geen volledige onafhankelijke frame-voor-frame videobeoordeling**. Tijden in de export zijn analysevoorstellen, geen bewezen wedstrijdenlementen. De getoonde moeilijkheidswaarden zijn waarden op het *ingediende blad*; ze zijn niet opnieuw door een jurylid vastgesteld.

## 1. Geplande elementen in volgorde

De negen ingevulde vakken staan als volgt op het wedstrijdblad:

| Nr. | Vak | Code op blad | Tijd/tekst op blad | Ingevulde waarde | Vergelijking met beschikbare export |
|---:|---:|---|---|---:|---|
| 1 | 1 | 1F | 3″ | 0,02 | Geen onafhankelijk geverifieerd videofragment; de AI-export bevat geen elementcodeherkenning. |
| 2 | 3 | B-AB, B-AB | combinatie van getekende bewegingen | — | Niet automatisch van dans of bewegingsverbinding te onderscheiden; tijdstip onbekend. |
| 3 | 5 | K-AI, K-AI | 2″ en 2″; op kaart als twee kaarsvormen afgebeeld | — | Bij 01:06,22–01:07,72 is *mogelijke kaars* door gebruiker bevestigd. Bij 01:59,69 ook. Kan zonder volledige videoreview niet aan dit specifieke kaartvak worden toegewezen. |
| 4 | 7 | 6C | ¼ vo | 0,03 | Nog geen betrouwbaar tijdstip; partnercontact op zichzelf is geen identificatie van 6C. |
| 5 | 9 | 2E | 1″–3″ | 0,03 | Nog geen betrouwbaar tijdstip; aanvang, uitvoering en eventuele houdingsduur afzonderlijk verifiëren. |
| 6 | 11 | T | figuurreeks op kaart | — | Niet verifieerbaar met alleen de huidige pose-uitvoer. |
| 7 | 13 | 5E | 0/4 ao | 0,02 | Nog geen betrouwbaar tijdstip; dynamische fasen apart herkennen. |
| 8 | 15 | 3D | 3″ | 0,02 | Nog geen betrouwbaar tijdstip; statische eindhouding en 3 s verifiëren. |
| 9 | 17 | 4F | 3″ | 0,02 | Nog geen betrouwbaar tijdstip; partnerconfiguratie en 3 s verifiëren. |

**Controle**: de zes ingevulde waarden tellen op tot 0,14. De kaart toont **Balans 0,09; Dynamisch 0,05; Individueel 0**. De waarden voor de niet-gewaardeerde vakken mogen niet alsnog opgeteld worden. Bladvolgorde is de *verwachte uitvoervolgorde*, maar bewijst niet dat een element daadwerkelijk is uitgevoerd.

## 2. Bestaande AI-reviewlabels op tijd

Uit v124: 

| Tijd (video) | Voorstel | Gebruikersreview | Voorzichtige interpretatie |
|---|---|---|---|
| 00:48,73 | mogelijk partnercontact | afgewezen | Geen kaartmatch |
| 01:04,22 | handstand en omgekeerde houding | afgewezen | Geen kaartmatch |
| 01:04,72–01:06,22 | partnercontact | bevestigd | Werkelijk contact is bevestigd, *exacte kaartcode onbekend* |
| 01:06,22–01:07,72 | kaars | bevestigd | Onderdeelsoort vermoedelijk overeenkomend met kaars-tekening in vak 5, maar geen bewezen directe match |
| 01:06,22–01:07,72 | algemene omgekeerde houding | afgewezen | Dubbeltelling van dezelfde lichaamshouding vermijden |
| 01:58,70 | partnercontact | nog open | Onzeker |
| 01:59,69 | kaars | bevestigd | Tweede kaarslabel; kan ander moment zijn of door pose-verwisseling ontstaan; kaartkoppeling open |
| 02:09,69 | partnercontact | bevestigd | Exacte elementcode onbekend |
| 02:17–02:25 | kaars en omgekeerd | afgewezen | Valse positieven, niet waarderen |

Een bevestigd AI-fragment is een menselijke controle van het *gemelde bewegingstype*; het is niet automatisch een bewijs van een specifieke moeilijke KNGU-code of een geldige houdingsduur. De verdichte AI-herkenning registreert voor de 01:06-kaars 0,84 s aaneengesloten positieve metingen, maar dit bewijst noch dat de feitelijke houding 0,84 s duurde, noch dat de vereiste 2 s gehaald zijn. Controleer de daadwerkelijke begin-/eindframes.

## 3. Meetbare regressie persoonsherkenning

De twee versies zijn op dezelfde video met 300 meetpunten getest:

| Metriek | v124 | v126 |
|---|---:|---:|
| Ten minste één pose geselecteerd | 79% | 44% |
| Verwachte formatie (twee poses) geselecteerd | 19% | 8% |
| Geautomatiseerde extra zoomscans | 1.032 | 1.937 |
| Meetpunten met onzekere rolkeuze | niet gerapporteerd | 289/300 |
| Mogelijke kaarsframes | 11 | 6 |

Deze metriek meet *het aantal poses*, niet of het werkelijk de twee gymnasten zijn. De scores 7,4/10 en 5,0/10 zijn **uitsluitend detecteerbaarheidsindicatoren**, geen juryscores. v126 mag niet als bewezen verbetering worden gepresenteerd. Het verschil kan mede door de handmatige werkgebiedinstellingen komen: v124 had een geselecteerd vlak, v126 `workArea=null`.

## 4. Selectie van een betere computer-visionengine

**Aanbevolen proefopzet A: persoon eerst herkennen, daarna pose.** Test twee onafhankelijke baselines op exact dezelfde video en dezelfde handmatige labels:

- **YOLO26-pose + BoT-SORT/OC-SORT**: meerdere personen per beeld, tracking-ID per gymnast. Voor sporten met snelle niet-lineaire bewegingen ook OC-SORT testen. ONNX-export is beschikbaar. Productdocumentatie: https://docs.ultralytics.com/tasks/pose en https://docs.ultralytics.com/modes/track. Let op AGPL-3.0-licentievoorwaarden voor niet-openbare distributie.
- **RTMDet + RTMPose**: eerst personen detecteren, daarna per persoon 17 lichaamspunten bepalen. Een browserimplementatie met ONNX Runtime Web is mogelijk: https://mmla.gse.harvard.edu/tools/rtmpose/ .
- **SAM 2.1 (of actuele SAM 3.1) optioneel**, als de bovenste persoon langdurig achter of vóór de onderste verdwijnt: twee personen op een beginframe selecteren en hun maskers door de video laten volgen. Dit is zwaarder en geen vervanging voor posepunten. https://ai.meta.com/research/sam2/ en https://ai.meta.com/blog/segment-anything-model-3/.

**Mijn technische voorkeursroute:** eerst RTMDet + RTMPose en YOLO26-pose als twee meetbare alternatieven, met per persoon een stabiele track-ID. Alleen bij moeilijke overlap SAM-tracking als tweede pass. MediaPipe uit v126 blijft een vergelijkingsbaseline totdat een alternatief aantoonbaar beter presteert. Dit is een modelkeuze, geen gemeten winnaar.

## 5. Volgorde-ondersteund herkennen

De wedstrijdkaart vormt een geordende lijst `1F → B-AB → K-AI → 6C → 2E → T → 5E → 3D → 4F`.

Algoritme:
1. Detecteer alle personen, niet hoogstens twee; houd hun tracks aan en onderscheid later op beweging, oefenvlak en samenhang. Een trainer mag niet stilzwijgend de plaats van een onzichtbare gymnast krijgen.
2. Segmentatie van video op mogelijke **elementvensters**, inclusief begin, stabiele middenfase en afbouw/landing. Dans/overgangen blijven een aparte klasse.
3. Vergelijk ieder venster met een **kaart-specifiek sjabloon**: top/base-positie, contactpunten, oriëntatie, rotatie, houddrempel, aantal deelnemers en volgorde.
4. Laat volgorde een voorkeur zijn, geen harde regel: overgeslagen/gewijzigde of verkeerd uitgevoerde elementen blijven mogelijk.
5. Meld per kaartvak `overeenkomst`, `mogelijke variant`, `niet gezien` of `onzeker`; ken pas een moeilijkheidswaarde toe met expliciete tabelversie, elementidentificatie én geldigheidscontrole.
6. Verwijder dubbele meldingen waarbij `kaars` en `omgekeerde houding` hetzelfde moment van dezelfde gymnast zijn.

**Validatie richting 90%**: begin met minstens ~150 handmatig gelabelde controlemomenten verspreid over de gehele video, plus dicht gelabelde overlap/kaars-momenten; houd testvideo's buiten training. Meet per gymnast recall, persoonswisselingen, trainer-als-gymnast-fouten, herkenning van werkelijk uitgevoerde elementen (precision/recall/F1) en correcte volgorde/koppeling van elementcode. Rapporteer werkelijke scores; geen hypothetische 90%-nauwkeurigheid claimen.

## Conclusie

Het wedstrijdblad is nu compleet als negen geordende verwachtingen vastgelegd. Voor vak 5 is een gerelateerd bevestigd kaarsvoorstel aanwezig, maar de directe koppeling aan dat specifieke element en de duur zijn niet bewezen. De andere vakken blijven zonder volledige videoweergave **niet geverifieerd**. Verbeter de persoonsdetectie eerst met een echte multiperson-detector, niet nog meer handgeschreven regels boven op één instabiele posebron.