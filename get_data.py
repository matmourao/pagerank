from bs4 import BeautifulSoup
import requests
import csv
import numpy as np

req = requests.get("https://esportes.estadao.com.br/classificacao/futebol/campeonato-brasileiro-serie-a/2021")
soup = BeautifulSoup(req.content, "html.parser")

data = open('data.csv', 'w', encoding='utf-8-sig')
writer = csv.writer(data)
header = ["rodada", "time1", "time2", "gol1", "gol2"]
writer.writerow(header)
partidas = []

for rodada in soup.find_all(class_="swiper-slide"):
    for jogo in rodada.find_all(class_="item"):
        row = [rodada.find(class_="table-fase").text]
        for time in jogo.find(class_="details").find_all(class_="shortname"):
            row.append(time.text)
        for gols in jogo.find(class_="details").find_all(class_="goal"):
            row.append(gols.text)
        writer.writerow(row)
        partidas.append(row)
data.close()

times = []
perdedores = []
vencedores = []
for partida in partidas:
    times.append(partida[1])

    if partida[3] < partida[4]:
        perdedores.append(partida[1])
        vencedores.append(partida[2])
    if partida[4] < partida[3]:
        perdedores.append(partida[2])
        vencedores.append(partida[1])
times = list(set(times))
times.sort()

arestas = []
for i in range(len(perdedores)):
  arestas.append([perdedores[i], vencedores[i]])

pesos = [0]*len(arestas)
for i in range(len(arestas)):
  if arestas[i] == []:
    continue
  for j in range(len(arestas)):
    if arestas[i] == arestas[j]:
      pesos[i] += 1
      if i != j:
        arestas[j] = []
for a in arestas:
  a.append(pesos[(arestas.index(a))])
arestas = list(filter(lambda x: x != [0], arestas))

with open("arestas.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["source","target","weight"])
    writer.writerows(arestas)

indice = {}
for i in range(len(times)):
  indice[times[i]] = i
for i in arestas:
  for j in range(2):
    i[j] = indice.get(i[j])

matriz = np.zeros((len(times), len(times)))
for a in arestas:
    i = a[0]
    j = a[1]
    matriz[i][j] = a[2]
print(matriz)
print(times)