import json
import hashlib
import matplotlib.pyplot as plt

class Lønsystem:
    def __init__(self):
        # Bed brugeren om at indtaste deres personlige timepris
        self.timepris = float(input("Indtast din personlige timepris (DKK pr. time): "))
        self.total_timer = 0  # Samlet antal timer arbejdet
        self.vagter = {}  # Dictionary til at gemme vagterne
        self.skat_procent = self.hent_skat_sats()  # Bed om skattesatsen én gang
        self.indlæs_vagter()  # Prøv at læse tidligere gemte vagter, hvis nogen

    def opdater_system(self):
        # Loop hvor brugeren kan vælge forskellige handlinger
        while True:
            valg = input("\nHvad vil du opdatere? (vagter, vis liste, rediger vagt, slet vagt, reset, vis løngraf, rediger profil, afslut): ").lower()

            if valg == "vagter":
                self.håndter_vagter()  # Opret eller opdater en vagt
            elif valg == "vis liste":
                self.vis_vagt_liste()  # Vis alle vagter med detaljer
                self.vis_total_løn()  # Vis samlet løn
            elif valg == "rediger vagt":
                self.rediger_vagt()  # Rediger eksisterende vagt
            elif valg == "slet vagt":
                self.slet_vagt()  # Slet vagt
            elif valg == "reset":
                self.reset_system()  # Nulstil systemet
            elif valg == "vis løngraf":
                self.vis_løngraf()  # Vis graf over samlet løn over tid
            elif valg == "rediger profil":
                self.rediger_profil()  # Rediger brugerprofil
            elif valg == "afslut":
                print("Programmet afsluttes.")
                break  # Afslut programmet
            else:
                print("Ugyldigt valg, prøv igen.")  # Hvis brugeren skriver noget ugyldigt

    def rediger_profil(self):
        # Funktion til at redigere brugerens profil
        print("\nRediger din profil:")
        while True:
            profil_valg = input("Hvad vil du redigere? (timepris, skat, tilbage): ").lower()
            if profil_valg == "timepris":
                try:
                    ny_timepris = float(input("Indtast din nye timepris (DKK pr. time): "))
                    self.timepris = ny_timepris
                    print(f"Din nye timepris er sat til {self.timepris:.2f} DKK pr. time.")
                    self.gem_vagter()  # Gem ændringen
                except ValueError:
                    print("Ugyldigt input. Indtast venligst et tal.")
            elif profil_valg == "skat":
                self.skat_procent = self.hent_skat_sats()
                print(f"Din skattesats er opdateret til {self.skat_procent * 100:.2f}%.")
                self.gem_vagter()  # Gem ændringen
            elif profil_valg == "tilbage":
                break
            else:
                print("Ugyldigt valg, prøv igen.")

    def håndter_vagter(self):
        # Funktion til at tilføje eller opdatere en vagt
        print("\nIndtast information for vagt:")
        dato = input("Dato (DD-MM-ÅÅÅÅ): ")
        timer = float(input("Antal arbejdstimer: "))
        minutter = float(input("Antal arbejdsminutter: "))

        tillæg = self.håndter_tillæg()

        total_minutter = timer * 60 + minutter
        self.total_timer += total_minutter
        self.vagter[dato] = {
            "antal_timer": total_minutter / 60,
            "skat_procent": self.skat_procent,
            "tillæg": tillæg
        }
        self.gem_vagter()

    def hent_skat_sats(self):
        skat_valg = input("\nHvilken skattesats vil du betale for denne vagt? (bund, tops eller selvvalgt): ").lower()
        if skat_valg == "tops":
            return 0.5202
        elif skat_valg == "bund":
            return 0.3842
        elif skat_valg == "selvvalgt":
            selvvalgt_skat = float(input("Indtast din ønskede skattesats i procent (f.eks. 40 for 40%): "))
            return selvvalgt_skat / 100
        else:
            print("Ugyldigt valg, antager normal skat sats (bund).")
            return 0.3842

    def håndter_tillæg(self):
        tillæg = 0
        tillæg_input = input("Ønsker du tillæg for et bestemt antal timer? (ja/nej): ").lower()
        if tillæg_input == "ja":
            tillæg_timer = float(input("Antal timer med tillæg: "))
            tillæg_beløb = float(input("Tillæg pr. time (i DKK): "))
            tillæg = tillæg_timer * tillæg_beløb
            print(f"Tillæg for det angivne antal timer: {tillæg:.2f} DKK")
        return tillæg

    def vis_vagt_liste(self):
        print("\nDatoer for vagter:")
        print("{:<15} {:<15} {:<20} {:<20} {:<20}".format("Dato", "Antal Timer", "Løn (DKK)", "Skat (DKK)", "Tillæg (DKK)"))

        for dato, info in self.vagter.items():
            skat_procent = info.get("skat_procent", 0.40)
            løn_efter_skat, skat = self.beregn_loen(info["antal_timer"] * 60, info.get("tillæg", 0), skat_procent)
            print("{:<15} {:<15.2f} timer {:<20.2f} {:<20.2f} {:<20.2f}".format(dato, info['antal_timer'], løn_efter_skat, skat, info["tillæg"]))

    def beregn_loen(self, løn_før_skat, tillæg=0, skat_procent=0.40):
        løn_før_skat = self.timepris * (løn_før_skat / 60)
        løn_før_skat += tillæg
        skat = løn_før_skat * skat_procent
        løn_efter_skat = løn_før_skat - skat
        return løn_efter_skat, skat

    def vis_total_løn(self):
        samlet_løn = sum([self.beregn_loen(vagt["antal_timer"] * 60, vagt.get("tillæg", 0), vagt.get("skat_procent", 0.40))[0] for vagt in self.vagter.values()])
        print("\nSamlet løn:")
        print(f"Samlet løn efter skat: {samlet_løn:.2f} DKK")

    def gem_vagter(self):
        try:
            with open("vagter.json", "w") as fil:
                json.dump({"total_timer": self.total_timer, "vagter": self.vagter, "skat_procent": self.skat_procent}, fil)
            print("Vagter gemt.")
        except Exception as e:
            print(f"Fejl ved gemning af data: {e}")

    def indlæs_vagter(self):
        try:
            with open("vagter.json", "r") as fil:
                data = json.load(fil)
                self.total_timer = data.get("total_timer", 0)
                self.vagter = data.get("vagter", {})
                self.skat_procent = data.get("skat_procent", 0.3842)
                print("\nVagter er indlæst.")
        except FileNotFoundError:
            print("\nIngen gemte vagter fundet.")
        except Exception as e:
            print(f"Fejl ved indlæsning af data: {e}")

    def rediger_vagt(self):
        print("\nRediger en eksisterende vagt:")
        dato = input("Indtast dato for vagten, du vil redigere (DD-MM-ÅÅÅÅ): ")

        if dato in self.vagter:
            print(f"Redigerer vagt for {dato}:")
            self.slet_vagt(dato)
            self.håndter_vagter()
        else:
            print("Ingen vagt fundet på den angivne dato.")

    def slet_vagt(self):
        print("\nSlet en vagt:")
        dato = input("Indtast dato for vagten, du vil slette (DD-MM-ÅÅÅÅ): ")

        if dato in self.vagter:
            del self.vagter[dato]
            self.gem_vagter()
            print(f"Vagt for {dato} slettet.")
        else:
            print("Ingen vagt fundet på den angivne dato.")

    def reset_system(self):
        self.total_timer = 0
        self.vagter = {}
        self.skat_procent = 0.3842
        self.gem_vagter()
        print("Systemet er blevet nulstillet.")
        
    def vis_løngraf(self):
        # Funktion til at vise en graf over kumulativ lønudvikling
        datoer = list(self.vagter.keys())
        kumulativ_løn = []
        total_løn = 0

        for dato in datoer:
            vagt = self.vagter[dato]
            løn_efter_skat, _ = self.beregn_loen(vagt["antal_timer"] * 60, vagt.get("tillæg", 0), vagt.get("skat_procent", 0.40))
            total_løn += løn_efter_skat  # Beregn den kumulative løn
            kumulativ_løn.append(total_løn)

        plt.figure(figsize=(10, 5))
        plt.plot(datoer, kumulativ_løn, marker="o")
        plt.xlabel("Dato")
        plt.ylabel("Kumulativ løn efter skat (DKK)")
        plt.title("Kumulativ lønudvikling over tid")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    system = Lønsystem()
    system.opdater_system()
