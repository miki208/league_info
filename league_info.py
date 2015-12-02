import urllib
import re
import math
import sys
import os

def poisson_distribution(X, lam):
    return (math.pow(math.e, -lam) * math.pow(lam, X)) / math.factorial(X)

def poisson_distribution1(X, lam): # F(x) = P{X <= x}
    sum = 0
    for i in range(0, X + 1, 1):
        sum += (math.pow(math.e, -lam) * math.pow(lam, i)) / math.factorial(i)
    return sum

def tacan_rezultat(h_avg, a_avg, rez1 = -1, rez2 = -1):
    if rez1 != -1 and rez2 != -1:
        argumenti = False
    else:
        argumenti = True
    if argumenti:
        rez = raw_input("Unesite rezultat u formatu rez1:rez2 - ").split(":")
        if len(rez) != 2:
            print "Morate uneti rezultat u formatu rez1:rez."
            return 0
        try:
            rez1 = int(rez[0])
            rez2 = int(rez[1])
        except ValueError:
            print "Rezultat mora biti numerickog tipa."
            return 0

    verovatnoca = poisson_distribution(rez1, home_avg) * poisson_distribution(rez2, away_avg)
    if argumenti:
        print "Verovatnoca da se utakmica zavrsi sa rezultatom %d:%d je %.2f%%." % (rez1, rez2, verovatnoca * 100)
    return verovatnoca

def izjednaceno(h_avg, a_avg):
    sum = 0
    for i in range(0, 8, 1):
        sum += tacan_rezultat(h_avg, a_avg, i, i)
    print "Verovatnoca da ce biti izjednaceno je %.2f%%." % (sum * 100)

def tacno_golovi(team_name, avg):
    try:
        rez = int(raw_input("Unesite broj golova koje treba da postigne %s: " % (team_name)))
    except ValueError:
        print "Broj golova mora biti numerickog tipa."
        return
    verovatnoca = poisson_distribution(rez, avg)
    print "Verovatnoca da ce %s postici %d golova je %.2f%%." % (team_name, rez, verovatnoca * 100)

def viseilijednako_golova(team_name, avg):
    try:
        rez = int(raw_input("Unesite koliko najmanje golova koje treba da postigne %s: " % (team_name)))
    except ValueError:
        print "Broj golova mora biti numerickog tipa."
        return
    verovatnoca = 1 - poisson_distribution1(rez - 1, avg)
    print "Verovatnoca da ce %s postici najmanje %d golova je %.2f%%." % (team_name, rez, verovatnoca * 100)

def manje_golova(team_name, avg):
    try:
        rez = int(raw_input("Unesite ispod koliko golova treba da postigne %s: " % (team_name)))
    except ValueError:
        print "Broj golova mora biti numerickog tipa."
        return
    verovatnoca = poisson_distribution1(rez - 1, avg)
    print "Verovatnoca da ce %s postici ispod %d golova je %.2f%%." % (team_name, rez, verovatnoca * 100)

def ukupno_najmanje(h_avg, a_avg):
    try:
        rez = int(raw_input("Unesite koliko najmanje golova treba da bude na utakmici: "))
    except ValueError:
        print "Broj golova mora biti numerickog tipa."
        return
    ishodi = [(x, y) for x in range(0, 8, 1) for y in range(0, 8, 1) if x + y <= rez - 1]
    sum = 0
    for x, y in ishodi:
        sum += tacan_rezultat(h_avg, a_avg, x, y)
    sum = 1 - sum
    print "Verovatnoca da ce na utakmici biti najmanje %d golova je %.2f%%." % (rez, sum * 100)

def ukupno_manjeod(h_avg, a_avg):
    try:
        rez = int(raw_input("Unesite ispod koliko golova treba da bude na utakmici: "))
    except ValueError:
        print "Broj golova mora biti numerickog tipa."
        return
    ishodi = [(x, y) for x in range(0, 8, 1) for y in range(0, 8, 1) if x + y <= rez - 1]
    sum = 0
    for x, y in ishodi:
        sum += tacan_rezultat(h_avg, a_avg, x, y)
    print "Verovatnoca da ce na utakmici biti manje od %d golova je %.2f%%." % (rez, sum * 100)

def pobedjuje_prvi(h_avg, a_avg, team_name):
    ishodi = [(x, y) for x in range(0, 8, 1) for y in range(0, 8, 1) if (x + y <= 10 and x > y)]
    sum = 0
    for x, y in ishodi:
        sum += tacan_rezultat(h_avg, a_avg, x, y)
    print "Verovatnoca da ce na utakmici pobediti %s je %.2f%%." % (team_name, sum * 100)

def pobedjuje_drugi(h_avg, a_avg, team_name):
    ishodi = [(x, y) for x in range(0, 8, 1) for y in range(0, 8, 1) if (x + y <= 10 and x < y)]
    sum = 0
    for x, y in ishodi:
        sum += tacan_rezultat(h_avg, a_avg, x, y)
    print "Verovatnoca da ce na utakmici pobediti %s je %.2f%%." % (team_name, sum * 100)

leagues = {
    "Spain Primera Division" : "http://www.fudbal91.com/fudbalska_statistika/Spain,_Primera_Division_(Liga_BBVA)/2014-2015",
    "Spain Segunda Division A" : "http://www.fudbal91.com/fudbalska_statistika/Spain,_Segunda_Division_A_(Liga_Adelante)/2014-2015",
    "Serbia Jelen Superliga" : "http://www.fudbal91.com/fudbalska_statistika/Serbia,_Jelen_Superliga/2014-2015"
}

if len(sys.argv) != 2 or sys.argv[1] not in leagues.keys():
    exit("Niste uneli naziv lige ili liga ne postoji u nasoj bazi.")

try:
    stream = urllib.urlopen(leagues[sys.argv[1]])
    data = stream.read()
    data = data.decode("utf-8")
    data = data.encode("ascii", "ignore")
    stream.close()
except IOError:
    exit("Sadrzaj ne moze da se preuzme!")

data = re.search(r"<tr id='standings_headrow'>.*?<tr id='standings_headrow'>.*?</tr>(.*?)</table>", data, re.S)
if data is None:
    exit("Greska prilikom parsiranja sadrzaja!")
data = data.group(1)
clubs = {}
regex = re.compile(r".*?<tr id='standings_row'>" +
                   r".*?<td class='l.*?<a.*?>(.*?)</a>" +     #naziv kluba
                   r".*?<td class='c.*?>(.*?)</td>"     +     #odigranih kuci
                   r".*?<td class='r.*?>(.*?)</td>"     +     #odnos postignutih i primljenih golova kuci
                   r".*?<td class='c.*?>(.*?)</td>"     +     #odigranih u gostima
                   r".*?<td class='r.*?>(.*?)</td>"     +     #odnos postignutih i primljenih golova u gostima
                   r".*?</tr>", re.S)
for m in regex.finditer(data): #0 odigrani kuci, 1 postignuti kuci, 2 primljeni kuci, 3 odigrani u gostima, 4 postignuti u gostima, 5 primljeni u gostima
    clubs[m.group(1)] = [int(m.group(2))]
    clubs[m.group(1)].extend(m.group(3).split(" : "))
    clubs[m.group(1)][1] = int(clubs[m.group(1)][1])
    clubs[m.group(1)][2] = int(clubs[m.group(1)][2])
    clubs[m.group(1)].append(int(m.group(4)))
    clubs[m.group(1)].extend(m.group(5).split(" : "))
    clubs[m.group(1)][4] = int(clubs[m.group(1)][4])
    clubs[m.group(1)][5] = int(clubs[m.group(1)][5])

numOfGames = 0
avg_home_scored = 0
avg_away_scored = 0
avg_home_conceded = 0
avg_away_conceded = 0
total_scored_home = 0
total_scored_away = 0
for k in clubs.keys():
    numOfGames += clubs[k][0]
    total_scored_home += clubs[k][1]
    total_scored_away += clubs[k][4]
avg_home_scored = (total_scored_home * 1.0) / numOfGames
avg_away_scored = (total_scored_away * 1.0) / numOfGames
avg_home_conceded = avg_away_scored
avg_away_conceded = avg_home_scored

#racunamo jacinu napada i odbrane za svaki tim
for k in clubs.keys():
    clubs[k].append(((clubs[k][1] * 1.0) / clubs[k][0]) / avg_home_scored) #6 dodajemo jacinu napada domacina
    clubs[k].append(((clubs[k][2] * 1.0) / clubs[k][0]) / avg_home_conceded) #7 dodajemo jacinu odbrane domacina
    clubs[k].append(((clubs[k][4] * 1.0) / clubs[k][3]) / avg_away_scored) #8 dodajemo jacinu napada u gostima
    clubs[k].append(((clubs[k][5] * 1.0) / clubs[k][3]) / avg_away_conceded) #9 dodajemo jacinu odbrane u gostima

close_app = False
while not close_app:
    data = raw_input("Unesite nazive klubova u formatu Domacin-Gost: ").split("-")
    os.system("cls")
    if len(data) != 2:
        print "Klubovi moraju biti u formatu Domacin-Gost."
        continue
    elif data[0] not in clubs.keys():
        print "Klub %s ne postoji u bazi." % (data[0])
        continue
    elif data[1] not in clubs.keys():
        print "Klub %s ne postoji u bazi." % (data[1])
        continue
    elif data[0] == data[1]:
        print "Nazivi klubova moraju biti razliciti."
        continue

    close_menu = False
    first = True
    while not close_menu:
        if first:
            first = False
            home_avg = clubs[data[0]][6] * clubs[data[1]][9] * avg_home_scored
            away_avg = clubs[data[1]][8] * clubs[data[0]][7] * avg_away_scored
        print data[0] + " - " + data[1]
        option = raw_input(("[1] - Verovatnoca da ce biti izjednaceno\n" +
                           "[2] - Verovatnoca za tacan rezultat\n" +
                           "[3] - Verovatnoca da %s postigne odredjen broj golova\n" +
                           "[4] - Verovatnoca da %s postigne odredjen broj golova\n" +
                           "[5] - Verovatnoca da %s postigne x+ golova\n" +
                           "[6] - Verovatnoca da %s postigne x+ golova\n" +
                           "[7] - Verovatnoca da %s postigne manje od x golova\n" +
                           "[8] - Verovatnoca da %s postigne manje od x golova\n" +
                           "[9] - Verovatnoca da ce ukupan broj golova biti najmanje x\n" +
                           "[10] - Verovatnoca da ce ukupan broj golova biti manji od x\n" +
                           "[11] - Verovatnoca da ce pobediti %s\n" +
                           "[12] - Verovatnoca da ce pobediti %s\n" +
                           "[13] - Izaberi druge timove\n" +
                           "[14] - Napusti aplikaciju\n") % (data[0], data[1], data[0], data[1], data[0], data[1], data[0], data[1]))

        os.system("cls")
        if option == "1":
            izjednaceno(home_avg, away_avg)
        elif option == "2":
            tacan_rezultat(home_avg, away_avg)
        elif option == "3":
            tacno_golovi(data[0], home_avg)
        elif option == "4":
            tacno_golovi(data[1], away_avg)
        elif option == "5":
            viseilijednako_golova(data[0], home_avg)
        elif option == "6":
            viseilijednako_golova(data[1], away_avg)
        elif option == "7":
            manje_golova(data[0], home_avg)
        elif option == "8":
            manje_golova(data[1], away_avg)
        elif option == "9":
            ukupno_najmanje(home_avg, away_avg)
        elif option == "10":
            ukupno_manjeod(home_avg, away_avg)
        elif option == "11":
            pobedjuje_prvi(home_avg, away_avg, data[0])
        elif option == "12":
            pobedjuje_drugi(home_avg, away_avg, data[1])
        elif option == "13":
            close_menu = True
            os.system("cls")
        elif option == "14":
            close_menu = True
            close_app = True
