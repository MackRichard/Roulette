import secrets
import time
import os
import msvcrt
#import winsound

farben = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m']

rot = "\033[31m█\033[0m"
schwarz = "\033[30m█\033[0m"
gruen = "\033[32m█\033[0m"

felderZahl = ["0 ","32","15","19","4 ","21","2 ","25","17","34","6 ","27","13","36","11","30","8 ","23","10","5 ","24","16","33","1 ","20","14","31","9 ","22","18","29","7 ","28","12","35","3 ","26"]
felderFarbe = [gruen,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz,rot,schwarz]

guthaben = 100
while True:
    while True:
        try:
            betMoney = int(input("Wie hoch ist dein Einsatz? "))
            if betMoney > guthaben:
                print(f"\033[31mDu besitzt nur {guthaben}$\033[0m")
                continue
            break
        except:
            print("\033[31mDas ist keine Zahl!\033[0m")
            continue

    betZahlSpeicher = []
    while True:
        bet = input("Worauf wettest du? [g,r,s,zahl] ")
        if bet == "zahl":
            while True:
                betZahl = input("Zahl hinzufügen [1-36]. \033[34m[ABBRUCH:ENTER]\033[0m")
                if betZahl in ["2","3","4","5","6","7","8","9"]:
                    betZahlSpeicher.append(betZahl + " ")
                    continue
                elif betZahl in felderZahl:
                    if betZahl in betZahlSpeicher:
                        print("\033[31mDiese Zahl wurde bereits hinzugefügt!\033[0m")
                        continue
                    else:
                        betZahlSpeicher.append(betZahl)
                        continue
                try:
                    if int(betZahl) >= 36:
                        print("\033[31mDiese Zahl ist zu hoch oder zu niedrig!\033[0m")
                        continue
                except:
                    if betZahl == "":
                        break
            if betZahlSpeicher == []:
                continue
        if bet not in ["g","r","s","zahl"]:
            print("\033[31mDarauf kann man nicht wetten!\033[0m")
            continue
        else:
            break
    guthaben-= betMoney

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"╔══════════════════════════\033[33mV\033[0m══════════════════════════╗")
    print("")
    print(f"╚══════════════════════════\033[33mɅ\033[0m══════════════════════════╝")

    print("\033[?25l", end="") #Cursor weg
    randomint = secrets.randbelow(100)+40
    i=0
    for j in range(randomint):
        fortschritt = j/randomint
        zeit = 0.03 + (fortschritt**3) * 0.8

        #winsound.Beep(2500, 50)

        feld1 = felderFarbe[(i+0) % 37]+felderZahl[(i+0) % 37]
        feld2 = felderFarbe[(i+1) % 37]+felderZahl[(i+1) % 37]
        feld3 = felderFarbe[(i+2) % 37]+felderZahl[(i+2) % 37]
        feld4 = felderFarbe[(i+3) % 37]+felderZahl[(i+3) % 37]
        feld5 = felderFarbe[(i+4) % 37]+felderZahl[(i+4) % 37]
        feld6 = felderFarbe[(i+5) % 37]+felderZahl[(i+5) % 37]
        feld7 = felderFarbe[(i+6) % 37]+felderZahl[(i+6) % 37]
        feld8 = felderFarbe[(i+7) % 37]+felderZahl[(i+7) % 37]
        feld9 = felderFarbe[(i+8) % 37]+felderZahl[(i+8) % 37]

        time.sleep(zeit)
        print(f"\033[2A\r║ {feld1} | {feld2} | {feld3} | {feld4} | {feld5} | {feld6} | {feld7} | {feld8} | {feld9} ║\033[K", end="\n\n")
        
        i+=1
    print("\033[?25h", end="") #Cursor wieder da

    farbeGewinn = felderFarbe[(i+3) % 37]

    gewählte_farbe = None
    if bet == "r":
        gewählte_farbe = rot
    elif bet == "s":
        gewählte_farbe = schwarz
    elif bet == "g":
        gewählte_farbe = gruen

    if gewählte_farbe == farbeGewinn == rot:
        guthaben += (betMoney*2)

        while True:
            farbe = secrets.choice(farben)
            print(f"\r{farbe}GEWINN!\033[0m \033[32m(+{betMoney*2}$)\033[0m \033[34m[ENTER]\033[0m", end="")

            time.sleep(0.2)
            if msvcrt.kbhit():
                msvcrt.getch()
                break
    elif gewählte_farbe == farbeGewinn == schwarz:
        guthaben += (betMoney*2)

        while True:
            farbe = secrets.choice(farben)
            print(f"\r{farbe}GEWINN!\033[0m \033[32m(+{betMoney*2}$)\033[0m \033[34m[ENTER]\033[0m", end="")

            time.sleep(0.2)
            if msvcrt.kbhit():
                msvcrt.getch()
                break
    elif gewählte_farbe == farbeGewinn == gruen:
        guthaben += (betMoney*36)

        while True:
            farbe = secrets.choice(farben)
            print(f"\r{farbe}GIGANTISCHER GEWINN!\033[0m \033[32m(+{betMoney*36}$)\033[0m \033[34m[ENTER]\033[0m", end="")

            time.sleep(0.2)
            if msvcrt.kbhit():
                msvcrt.getch()
                break
    elif felderZahl[(i+3) % 37] in betZahlSpeicher:
        guthaben += (betMoney*((35/len(betZahlSpeicher))-2))
        while True:
            farbe = secrets.choice(farben)
            print(f"\r{farbe}RIESIGER GEWINN!\033[0m \033[32m(+{betMoney*(35/len(betZahlSpeicher))}$)\033[0m \033[34m[ENTER]\033[0m", end="")

            time.sleep(0.2)
            if msvcrt.kbhit():
                msvcrt.getch()
                break
    else:
        print("Du hast leider verloren.")

    while guthaben > 0:
        print("\033[?25h", end="") #Cursor wieder da
        erneut = input("\033[2A\n\nNoch einmal? \033[34m[ENTER]\033[0m\033[K").lower()
        if erneut == "cash":
            os.system('cls' if os.name == 'nt' else 'clear')
            geld_str = f"{guthaben}$"
            print("╔═════════════════════════╗")
            print("║        \033[4mGuthaben\033[0m:        ║")
            print(f"║\033[32m{geld_str:^25}\033[0m║")
            print("╚═════════════════════════╝")
            continue
        elif erneut == "gewinne":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("╔══════════════════════════════╗")
            print("║           \033[4mGewinne\033[0m:           ║")
            print("║ \033[31mROT\033[0m: Einsatz x 2$            ║")
            print("║ \033[30mSCHWARZ\033[0m: Einsatz x 2$        ║")
            print(f"║ \033[32mGRÜN\033[0m: \033[33mEinsatz x 36$\033[0m          ║")
            print("║ \033[35mZAHL\033[0m: \033[33mEinsatz x 35$\033[0m          ║")
            print("╚══════════════════════════════╝")
            continue
        elif erneut == "":
            break
        else:
            print(f"Danke, für's Spielen. Dein Guthaben beträgt: \033[32m{guthaben}$\033[0m")
            exit()
