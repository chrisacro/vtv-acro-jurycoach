# Proefplan: herkenning element 2A zonder persoonsverwarring

**Doel:** Jurycoach herkent in een duo twee afzonderlijke gymnasten bij een horizontale heffing (vliegtuigje) vóórdat het systeem elementcode 2A suggereert.

## Controlefragment
- Supplement 2, damesduo, één proefelement.
- Testvenster **00:25–00:41** (feitelijke elementfase in de handmatige tijdlijn circa **00:28–00:38**).
- Referentie: beide gymnasten doen mee; bovenpartner horizontaal, onderpartner draagt.
- De bronvideo, afbeeldingen en persoonsgegevens worden **niet** in deze openbare repository gezet.

## Verplichte volgorde
1. Selecteer de **twee echte gymnasten** aan het begin en ken hun vaste spoor-ID's toe.
2. Voer multiperson-detectie uit bij meerdere beeldschalen; bewaar identiteit over opeenvolgende frames.
3. Bij overlap of één ontbrekende pose: markeer **onzeker**, nooit een trainer of derde persoon als vervanger.
4. Controleer pas bij twee betrouwbaar gevolgde personen de horizontale bovenpartner, rechtopstaande onderpartner, relatieve hoogte en ondersteuningscontact.
5. Rapporteer **'mogelijk 2A'** als kandidaat, geen automatisch erkende moeilijkheid of KNGU-score.
6. Vergelijk na afloop de AI-uitkomst met de handmatige referentie; geef false positives, gemiste frames en persoonswisselingen afzonderlijk weer.

## Vergelijking
Test twee trackingsystemen met **dezelfde video, hetzelfde posemodel, dezelfde beelden en dezelfde selectiestart**. Bijvoorbeeld ByteTrack en BoT-SORT. Meet:
- aandeel frames met twee afzonderlijke, **daadwerkelijk juiste** gymnasten;
- fouten door verwisseling met derden;
- identiteitswisselingen vóór, tijdens en na overlap;
- percentage **onzeker**; en
- aantal correcte en foutieve 2A-kandidaten.

Handmatige controle is vereist: twee aanwezige track-ID's alleen bewijzen de identiteit niet.

## Acceptatiecriteria (streefwaarden, niet behaald)
- Beiden als juiste gymnasten herkend: **≥95%** van de relevante meetframes.
- Persoonswisselingen: **0**.
- Trainer ten onrechte geselecteerd: **0**.
- 2A-kandidaat alleen wanneer de lichaamshouding dit ondersteunt; geen label bij ontbrekende personen.

## Huidige status
De proef is **gespecificeerd**, nog **niet op echte AI-resultaten gevalideerd**. Synthetische zelftests van een apart lokaal proefscript zijn geslaagd; ze bewijzen geen herkenningsnauwkeurigheid op de opname. Eerst dit element betrouwbaar krijgen, daarna pas generaliseren naar andere kaartvakken.
