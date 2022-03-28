Damit der main Thread für den Bot laufen kann, benötigt man einen HTTP Server (hier mit Flask) und eine Überwachung, die den Webserver regelmäßig requests schickt, damit der nach 30 Minuten nicht in den Sleep zustand wechselt (z.B. UptimeRobot)  

Currently hostet at:  
https://replit.com/@andre360/TTT#main.py  
  
Service Monitoring with:  
https://uptimerobot.com/



"""
Define command palette for Telegram Client
1. Nachricht an @BotFather mit /setcommands
2. Bot auswählen
3. senden: 

newgame - Erstelle neue leere Lobby
startgame - Startet das aktuelle Spiel
signup - Am aktuellen Spiel teilnehmen
signout - Aus aktuellem Spiel abmelden

"""


Set Windows Enviroiment Variable
Powershell: `$Env:TOKEN = "telegram_token..."`