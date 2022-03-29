# Lasertag Telegram-Bot

## Projekt
Um im Freundeskreis Lasertag mit Rollen, nach dem Prinzip des Spiels TTT (Trouble in Terrorist Town) zu spielen. Anstelle einer App wurde hier auf einen Telegram Bot gesetzt, da so nur ein kleines "Backend" benötigt wird.



## Das Spiel
### Spiel erstellen

Bei `/newgame` können die Namen für Rollen beliebig vergeben werden. 
Lediglich Jester und Traitor müssen korrekt geschrieben werden, da diesen eine
separate Funktion hinterliegt. Den restlichen Spielern wird die Rolle `Unschuldig` zugeteilt.

z.B. sechs Spieler:  
`/newgame Traitor:2 Jester:1Z` 
```JSON
{
    "Traitor": ["spieler_5", "spieler_1"],
    "Jester": ["spieler_4"],
    "Unschuldig": ["spieler_6", "spieler_2", "..."]
}
```

### Spiel beitreten
Sobald ein Spiel erstellt wurde, können andere Mitspieler der Gruppe mit `/signup` dem Spiel beitreten

### Spiel starten
Mit `/startgame` wird das Spiel gestartet und die Spieler bekommen eine Direkt Nachricht, welche Rolle ihnen zugeteilt wurde.  
Die Traitor bekommen zusätzlich mitgeteilt, wer die anderen Traitor, sowie Jester sind.  
Dieser befehl kann beliebig oft wiederholt werden. Um die Rollen zu ändern muss ein neues Spiel erstellt werden

### Spiel verlassen
Falls ein Mitspieler nicht mehr an der "Rollenvergabe" des aktuellen Spieles teilnehmen möchte, kann er mit `/signout` die aktuelle Lobby verlassen



## Telegram Bot

### Commands definieren
In der Telegramm App wird ein Button angezeigt, welcher alle verfügbaren Befehle auflistet.

1. Nachricht an @BotFather mit `/setcommands`
2. Bot auswählen
3. folgende Beschreibung senden:  
```
newgame - Erstelle neue leere Lobby
startgame - Startet das aktuelle Spiel
signup - Am aktuellen Spiel teilnehmen
signout - Aus aktuellem Spiel abmelden
```



## Sonstiges
- Falls ein Spieler zum ersten mal spielt, muss er dem Bot zuerst eine Nachricht persönlich senden


## Development
### Set environment variables
```bash
vi ~/.bash_profile
export TOKEN=myToken
source ~/.bash_profile
```

### Install Python dependencies
```bash
pip install -r requirements.txt
```

## Production
Using Docker  
```bash
docker build --tag lasertag-bot .
docker run -e TOKEN=mytoken lasertag-bot
```

