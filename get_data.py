from bs4 import BeautifulSoup
import requests
import csv

req = requests.get("https://esportes.estadao.com.br/classificacao/futebol/campeonato-brasileiro-serie-a/2021")
soup = BeautifulSoup(req.content, "html.parser")

data = open('data.csv', 'w', encoding='utf-8-sig')
writer = csv.writer(data)
header = ["rodada", "time1", "time2", "gol1", "gol2"]
writer.writerow(header)

for rodada in soup.find_all(class_="swiper-slide"):
    for jogo in rodada.find_all(class_="item"):
        row = [rodada.find(class_="table-fase").text]
        for time in jogo.find(class_="details").find_all(class_="shortname"):
            row.append(time.text)
        for gols in jogo.find(class_="details").find_all(class_="goal"):
            row.append(gols.text)
        writer.writerow(row)
   
data.close()