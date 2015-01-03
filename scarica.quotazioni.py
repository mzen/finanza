import csv

with open('listino.csv', 'r') as listino:
    rider = csv.reader(listino, delimiter=',')
    with open('scarica.sh', 'w') as scell:
        for elem in rider:
            titolo = elem[0].lower()
            if titolo == 'codice':
                continue
            else:
                print titolo
                # Recupero lo storico disponibile ad oggi
                url = "wget -O %s.csv http://real-chart.finance.yahoo.com/table.csv?s=%s\n" % (titolo, titolo)
                scell.write(url)
                if len(elem[1]) > 0:
                    # Recupero i dividendi fino ad oggi
                    url = "wget -O %s.div.csv 'http://real-chart.finance.yahoo.com/table.csv?s=%s&g=v'\n" % (titolo, titolo)
                    scell.write(url)
                else:
                    continue
