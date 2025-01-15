import bcrypt

# Gem brugernavne og hashede adgangskoder
brugere = {}
er_logget_ind = False  # Flag for at kontrollere, om brugeren er logget ind

def opret_konto():
    brugernavn = input("Indtast et brugernavn: ")
    adgangskode = input("Indtast en adgangskode: ")
    
    # Generer et salt og hash adgangskoden
    salt = bcrypt.gensalt()
    hashed_adgangskode = bcrypt.hashpw(adgangskode.encode(), salt)
    
    # Gem brugeren med den saltede og hashede adgangskode
    brugere[brugernavn] = hashed_adgangskode
    print(f"Konto oprettet for {brugernavn}.")

def login():
    global er_logget_ind
    brugernavn = input("Indtast brugernavn: ")
    adgangskode = input("Indtast adgangskode: ")
    
    # Tjek om brugeren findes
    if brugernavn in brugere:
        hashed_adgangskode = brugere[brugernavn]
        
        # Sammenlign adgangskoden med den gemte hash
        if bcrypt.checkpw(adgangskode.encode(), hashed_adgangskode):
            er_logget_ind = True
            aktiver_lønberegner()
        else:
            print("Forkert adgangskode.")
    else:
        print("Brugernavn findes ikke.")

def aktiver_lønberegner():
    print("\nVelkommen til lønberegneren!")
    try:
        exec(open("lønberegner.py").read())
    except FileNotFoundError:
        print("Filen 'lønberegner.py' blev ikke fundet. Sørg for, at den er placeret i samme mappe som dette script.")
    except Exception as e:
        print(f"Der opstod en fejl under kørsel af 'lønberegner.py': {e}")


def menu():
    global er_logget_ind
    while True:
        if not er_logget_ind:
            valg = input("\nVælg en handling (opret, login, afslut): ").lower()
            
            if valg == "opret":
                opret_konto()
            elif valg == "login":
                login()
            elif valg == "afslut":
                print("Programmet afsluttes.")
                break
            else:
                print("Ugyldigt valg, prøv igen.")
        else:
            break
        

# Start programmet
menu()
