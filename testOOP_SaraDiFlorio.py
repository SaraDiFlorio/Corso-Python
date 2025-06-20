'''
Test Finale OOP : "La Battaglia dei Regni"
Realizzato da: SARA DI FLORIO
'''

# Istruzioni: 2 giocatori in totale (un giocatore contro una IA). Ogni giocatore ha un budget di 1000 monete inizialmente. 
# Attacco e difesa di ogni tipo di soldato sono in un range di punti impostato di default e compreso tra (0,50) (non li può scegliere l'utente).
# Stato di salute massimo pari a 100 punti e posto pari al massimo per ogni tipo di soldato all'inizio della battaglia.


from abc import ABC, abstractmethod
import random



# ------------------------------- CLASSI -------------------------------



class Soldato(ABC):
    def __init__(self, nome, costo, attacco, difesa, salute):
        self.__nome = nome
        self.__costo = costo
        self.__attacco = attacco
        self.__difesa = difesa
        self.__salute = salute
    
    def difenditi(self, danno):
        danno_vero = max(0, danno - self.__difesa)
        self.__salute = max(0, self.__salute - danno_vero)
        print(f"{self.__nome.upper()} ha subito {danno_vero} danni. Salute attuale: {self.__salute}")
        
    def e_vivo(self):
        return self.__salute > 0

    def stato(self):
        print(f"{self.__nome.upper()}, stato di salute: {self.__salute}")

    def get_nome(self):
        return self.__nome
    
    def get_costo(self):
        return self.__costo
    
    def get_attacco(self):
        return self.__attacco
    
    def get_difesa(self):
        return self.__difesa
    
    def get_salute(self):
        return self.__salute
    
    def set_salute(self,newSalute):
        self.__salute = newSalute
        return self.__salute
    
    def __str__(self):
        return f"{self.__nome}{self.__costo}{self.__attacco}{self.__difesa}{self.__salute}"

    @abstractmethod
    def attacca(self, avversario):
        pass


class Cavaliere(Soldato):
    def __init__(self, nome):
        super().__init__(nome, 200, 25, 40, 100)  #costo alto, attacco medio, difesa alta
    
    #20% di possibilità di colpo critico (attacco x 2)
    def attacca(self, avversario):
        print(f"{self.get_nome().upper()} attacca {avversario.get_nome().upper()}")
        danno = self.get_attacco()
        avversario.difenditi(danno)
        if random.random() < 0.2:        
            print(f"{self.get_nome().upper()} esegue colpo critico!")
            avversario.difenditi(danno)


class Arciere(Soldato):
    def __init__(self, nome):
        super().__init__(nome, 120, 40, 15, 100)  #costo medio, attacco alto, difesa bassa 

    #attacca per primo in ogni scontro 1 vs 1  (condizione implementata nella logica di gioco in seguito)
    def attacca(self, avversario):
        print(f"{self.get_nome().upper()} attacca per primo {avversario.get_nome().upper()}")
        danno = self.get_attacco()
        avversario.difenditi(danno)


class Guaritore(Soldato):
    def __init__(self, nome):
        super().__init__(nome, 120, 15, 15, 100)  #costo medio, attacco basso, difesa bassa
    
    #invece di attaccare, cura un alleato vivo random (aggiunge 20 punti alla salute dell'alleato, se minore del massimo impostato, cioè di 100)
    def attacca(self, alleati):
        alleati_vivi = [el for el in alleati if el != self and el.e_vivo()]
        if alleati_vivi:
            scelta_alleato = random.choice(alleati_vivi)
            newSalute = min(100, scelta_alleato.get_salute() + 20)
            scelta_alleato.set_salute(newSalute)
            print(f"{self.get_nome().upper()} cura {scelta_alleato.get_nome().upper()}! Salute: {scelta_alleato.get_salute()}")
        else: 
            print(f"{self.get_nome().upper()} non ha nessuno da curare!")


class Mago(Soldato):
    def __init__(self, nome):
        super().__init__(nome, 180, 10, 15, 100)  #costo alto, attacco variabile (10-40), difesa bassa
    
    #probabilità di non attaccare ma di saltare il turno per stanchezza, del 25%
    def attacca(self, avversario):
        if random.random() < 0.25:        
            print(f"{self.get_nome().upper()} salta il turno per stanchezza!")
            avversario.difenditi(0)
        else:
            print(f"{self.get_nome().upper()} attacca {avversario.get_nome().upper()}")
            attacco_vero = self.get_attacco() + random.randint(0,30)
            danno = attacco_vero
            avversario.difenditi(danno)



# ------------------------------- FUNZIONI -------------------------------



def crea_esercito_giocatore(budget):
    print("Acquista i tuoi soldati per il round!")
    esercito_giocatore = []
    i = 1
    while budget >= 120: #costo più basso possibile per i tipi di soldati (Arciere e Guaritore costano 120, gli altri di più)
        nome = (input(f"Inserisci il nome del soldato {i}: "))
        tipo = input("Inserisci il tipo di soldato:\n1 per Cavaliere (200 monete)\n2 per Arciere (120 monete)\n3 per Guaritore (120 monete)\n4 per Mago (180 monete): ")
        if tipo == "1": 
            soldato = Cavaliere(nome)
        elif tipo == "2":
            soldato = Arciere(nome)
        elif tipo == "3":
            soldato = Guaritore(nome)
        elif tipo == "4":
            soldato = Mago(nome)
        else:
            print("Inserire un numero da 1 a 4 per scegliere il tipo di soldato!")
            continue

        if budget >= soldato.get_costo():
                esercito_giocatore.append(soldato)
                budget -= soldato.get_costo()
                print(f"Soldato acquistato! Budget rimanente: {budget} monete.")
        else:
            print("Budget insufficiente per questo tipo di soldato!")
       
        i += 1

    return esercito_giocatore, budget


def crea_esercito_IA(budget):
    esercito_IA = []
    while budget >= 120: 
        nome_cavaliere = f"Cavaliere {random.randint(1,100)}"
        nome_arciere = f"Arciere {random.randint(1,100)}"
        nome_guaritore = f"Guaritore {random.randint(1,100)}"
        nome_mago = f"Mago {random.randint(1,100)}"
        tipo = random.choice([1,2,3,4])
        if tipo == 1: 
            soldato = Cavaliere(nome_cavaliere)
        elif tipo == 2:
            soldato = Arciere(nome_arciere)
        elif tipo == 3:
            soldato = Guaritore(nome_guaritore)
        elif tipo == 4:
            soldato = Mago(nome_mago)
        
        if budget >= soldato.get_costo():
            esercito_IA.append(soldato)
            budget -= soldato.get_costo()
        else:
            break

    return esercito_IA, budget


#funzione per il singolo duello
def duello(soldato1, soldato2):      
    turno = 1
    max_turni = 50 #limite massimo di turni di attacco e difesa per ogni duello

    #Caso 1: se entrambi i soldati sono guaritori non duellano
    if isinstance(soldato1, Guaritore) and isinstance(soldato2, Guaritore):
        print(f"{soldato1.get_nome().upper()} e {soldato2.get_nome().upper()} sono entrambi guaritori e non duellano.")
        return None
    
    #Caso 2: se uno dei due è guaritore, lui non attacca e l'altro lo attacca finchè non muore
    if isinstance(soldato1, Guaritore):
        print(f"{soldato1.get_nome().upper()} è un guaritore e non attacca, {soldato2.get_nome().upper()} attacca finché il guaritore muore.")
        while soldato1.e_vivo() and soldato2.e_vivo():
            soldato2.attacca(soldato1)
        return soldato2 if soldato2.e_vivo() else None
    if isinstance(soldato2, Guaritore):
        print(f"{soldato2.get_nome().upper()} è un guaritore e non attacca, {soldato1.get_nome().upper()} attacca finché il guaritore muore.")
        while soldato1.e_vivo() and soldato2.e_vivo():
            soldato1.attacca(soldato2)
        return soldato1 if soldato1.e_vivo() else None

    #Caso 3: duello normale
    while soldato1.e_vivo() and soldato2.e_vivo() and turno <= max_turni: 
        #Arciere attacca sempre per primo, se presente
        if turno == 1:
            if isinstance(soldato1, Arciere):
                soldato1.attacca(soldato2)
            elif isinstance(soldato2, Arciere):
                soldato2.attacca(soldato1)
            else: 
                soldato1.attacca(soldato2) #Nessun arciere, attacca soldato 1 per primo
        
        else: 
            if turno % 2 == 0:
                soldato1.attacca(soldato2)
            else: 
                soldato2.attacca(soldato1)
        turno +=1

        if turno > max_turni:
            print(f"Duello tra {soldato1.get_nome().upper()} e {soldato2.get_nome().upper()} terminato per limite turni superato.")
            vincitore = random.choice([soldato1, soldato2])
            print(f"Vincitore a sorte: {vincitore.get_nome().upper()}")
            return vincitore
        
    if soldato1.e_vivo():
        vincitore = soldato1
    elif soldato2.e_vivo(): 
        vincitore = soldato2
    else: vincitore = None
    return vincitore       


#funzione per la battaglia vera e propria e la gestione dei round 
def battaglia(esercito_giocatore,esercito_IA, budget_giocatore, budget_IA): 
    numero_scontro = 1
    while True:

        # Controllo a inizio round: eserciti vuoti o solo guaritori
        if len(esercito_giocatore) == 0:
            print("Vince IA!")
            break
        if len(esercito_IA) == 0:
            print("Vince giocatore!")
            break

        if esercito_giocatore and all(isinstance(el, Guaritore) for el in esercito_giocatore):
            print("Battaglia terminata: l'esercito del Giocatore ha solo guaritori.")
            break
        if esercito_IA and all(isinstance(el, Guaritore) for el in esercito_IA):
            print("Battaglia terminata: l'esercito dell'IA ha solo guaritori.")
            break
        
        # recap soldati e budget a inizio di ogni round
        print(f"\n--- INIZIO ROUND {numero_scontro} ---")
        print("Giocatore - Esercito corrente:")
        for soldato in esercito_giocatore:
            tipo = type(soldato).__name__
            print(f"  {soldato.get_nome().upper()} - {tipo} (Salute: {soldato.get_salute()})")
        print(f"Budget Giocatore: {budget_giocatore} monete\n")

        print("IA - Esercito corrente:")
        for soldato in esercito_IA:
            tipo = type(soldato).__name__
            print(f"  {soldato.get_nome().upper()} - {tipo} (Salute: {soldato.get_salute()})")
        print(f"Budget IA: {budget_IA} monete")
        print("-------------------\n")
    
        vincitori_giocatore = []
        vincitori_IA = []
        
        min_lunghezza = min(len(esercito_giocatore), len(esercito_IA))

        for i in range (min_lunghezza):
            soldato1 = esercito_giocatore[i]
            soldato2 = esercito_IA[i]

            if isinstance(soldato1, Guaritore):   #se ci sono guaritori, questi curano qualcuno degli alleati a inizio round in modo randomico
                soldato1.attacca(esercito_giocatore)
            if isinstance(soldato2, Guaritore):
                soldato2.attacca(esercito_IA)
            
            #se entrambi sono guaritori non duellano
            if isinstance(soldato1, Guaritore) and isinstance(soldato2, Guaritore):
                pass
            else:
                vincitore = duello(soldato1, soldato2)
                if vincitore == soldato1 and soldato1.e_vivo():
                    vincitori_giocatore.append(soldato1)
                elif vincitore == soldato2 and soldato2.e_vivo():
                    vincitori_IA.append(soldato2)
            
        vincitori_giocatore += esercito_giocatore[min_lunghezza:]  
        vincitori_IA += esercito_IA[min_lunghezza:]

        esercito_giocatore = vincitori_giocatore
        esercito_IA = vincitori_IA

        budget_giocatore += 300   #alla fine del round ogni giocatore riceve 300 monete che si sommano al budget eventuale residuo
        budget_IA += 300

        # recap soldati e budget a fine di ogni round
        print(f"\n--- FINE ROUND {numero_scontro} ---")
        print("Soldati rimasti - GIOCATORE:")
        for soldato in esercito_giocatore:
            tipo = type(soldato).__name__
            print(f"{soldato.get_nome().upper()} - {tipo} (Salute: {soldato.get_salute()})")
        print(f"Budget Giocatore: {budget_giocatore} monete")

        print("\nSoldati rimasti - IA:")
        for soldato in esercito_IA:
            tipo = type(soldato).__name__
            print(f"{soldato.get_nome().upper()} - {tipo} (Salute: {soldato.get_salute()})")
        print(f"Budget IA: {budget_IA} monete")
        print("-------------------\n")

        # Controllo a fine round se uno dei due eserciti è vuoto
        if len(esercito_giocatore) == 0:
            print(f"---> Il vincitore è l'IA!\nNumero round giocati: {numero_scontro}\n"
                f"Soldati rimasti IA: {len(esercito_IA)}\nSoldati rimasti Giocatore: 0")
            break
        if len(esercito_IA) == 0:
            print(f"---> Il vincitore è il giocatore!\nNumero round giocati: {numero_scontro}\n"
                f"Soldati rimasti Giocatore: {len(esercito_giocatore)}\nSoldati rimasti IA: 0")
            break

        nuovi_soldati_giocatore, budget_giocatore = crea_esercito_giocatore(budget_giocatore)    #e può acquistare nuovi soldati
        esercito_giocatore += nuovi_soldati_giocatore
        nuovi_soldati_IA, budget_IA = crea_esercito_IA(budget_IA)
        esercito_IA += nuovi_soldati_IA

        numero_scontro +=1 
    


# ------------------------------- IMPLEMENTAZIONE -------------------------------



print("Benvenuto alla 'Battaglia dei Regni'. Preparati a combattere! Budget iniziale: 1000 monete")

budget_iniziale = 1000
esercitoGiocatore, budget_giocatore = crea_esercito_giocatore(budget_iniziale)
esercitoIA, budget_IA = crea_esercito_IA(budget_iniziale)

battaglia(esercitoGiocatore, esercitoIA, budget_giocatore, budget_IA)
        
    
        


        
        




