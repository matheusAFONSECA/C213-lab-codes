
import re                       # Suporte para reconhecimento de expressões regulares.
import itertools                # Suporte para operações iterativas.
import numpy as np              # Suporte para operações matemáticas.
import pandas as pd             # Suporte para manipulação de DataFrames.
import skfuzzy as fuzzy         # Suporte para operação com Lógica Fuzzy.
import skfuzzy.control as ctrl  # Suporte para manipulação de Sistemas Fuzzy.
import matplotlib.pyplot as plt # Suporte para visualização de gráficos.

from tabulate import tabulate   # Suporte para manipulação de Tabelas.
vermelho, verde, amarelo, azul, magenta, ciano = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']

# Definição da variável Antecedente Velocidade 0:120 km/h
Velocidade = ctrl.Antecedent(universe=np.arange(0, 121, 1), label='Velocidade')

# Classificações de Velocidade em MB, B, M, A e MA.
Velocidade['MB'] = fuzzy.trapmf(Velocidade.universe, [0, 0, 20, 40])
Velocidade['B'] = fuzzy.trimf(Velocidade.universe, [20, 40, 60])
Velocidade['M'] = fuzzy.trimf(Velocidade.universe, [40, 60, 80])
Velocidade['A'] = fuzzy.trimf(Velocidade.universe, [60, 80, 100])
Velocidade['MA'] = fuzzy.trapmf(Velocidade.universe, [80, 100, 120, 120])

Velocidade.view()   # Método para visualização da Função de Pertinência.
[plt.gca().lines[i].set_linewidth(2) for i in range(len(plt.gca().lines))]

fig = plt.gcf(); axes = fig.gca(); fig.set_size_inches(6, 2)
axes.set_xlabel(xlabel=f'{Velocidade.label} [km/h]'); axes.set_ylabel(ylabel='Pertinência $\mu_{V}$')
plt.title(f'Classificações para a varável {Velocidade.label}', fontweight='bold'); plt.legend(loc='upper right')

# Faça a Fuzzyficação da Variável Inclinação aqui.

# Faça a Fuzzyficação da Variável Aceleração aqui.

# Regras para condição de Velocidade MB e variação da Inclinação:
R1 = ctrl.Rule(Velocidade['MB'] & Inclinacao['MN'], Aceleracao['P'])
R2 = ctrl.Rule(Velocidade['MB'] & Inclinacao['PN'], Aceleracao['M'])
R3 = ctrl.Rule(Velocidade['MB'] & Inclinacao['ZE'], Aceleracao['A'])
R4 = ctrl.Rule(Velocidade['MB'] & Inclinacao['PP'], Aceleracao['A'])
R5 = ctrl.Rule(Velocidade['MB'] & Inclinacao['MP'], Aceleracao['MA'])

# Complete a Base com as demais 20 regras.
# Utilize nomes padronizados para as variáveis.

# Monte a Base de Regras aqui.

tabela = []
for velocidade in Velocidade.terms:
  for inclinacao in Inclinacao.terms:
    for regra in BaseRegras:
      antecedente = str(regra).split('IF ')[1].split(' THEN')[0].replace('AND ', '')
      consequente = str(regra).split('IF ')[1].split(' THEN')[1].split('AND ')[0]

      classificacoes = re.findall(r'\[(.*?)\]', (antecedente + consequente))
      if velocidade == classificacoes[0] and inclinacao == classificacoes[1]:
        tabela.append([classificacoes[0], classificacoes[1], classificacoes[2]])
        break

df = pd.DataFrame(tabela, columns=[Velocidade.label, 'E', Aceleracao.label])
pivotTable = pd.DataFrame(df.pivot(index='E', columns=Velocidade.label, values=Aceleracao.label).reindex(index=Inclinacao.terms, columns=Velocidade.terms))
pivotTable.index.name = f'{ciano}{pivotTable.index.name}\033[0m'
print(tabulate(pivotTable, headers='keys', tablefmt='fancy_grid', stralign='center', showindex='always'), end='\n\n')

# Print uma regra qualquer e observe como ela é interpretada.

ControleVelocidade = ctrl.ControlSystemSimulation(ctrl.ControlSystem(BaseRegras))
ControleVelocidade.input[Velocidade.label] = 0  # Escolha um input para a Velocidade.
ControleVelocidade.input[Inclinacao.label] = 0  # Escolha um input para a Inclinação.
ControleVelocidade.compute()

# Resgate os valores das Variáveis de Entrada aqui.

# Graus de pertinência para a variável Velocidade:
ativacaoVelocidade = []   # Regiões ativadas para a Velocidade.
for velocidade in Velocidade.terms:
  uV = fuzzy.interp_membership(Velocidade.universe, Velocidade[velocidade].mf, ControleVelocidade._get_inputs()[Velocidade.label])
  if uV != 0:
    print(f'Pertinência {velocidade}: {uV:.2f}')
    ativacaoVelocidade.append(velocidade)

# Compute os valores da Variável Inclinação aqui.

# Verifique as classificações da Variável de Saída aqui.

Aceleracao.view(sim=ControleVelocidade)
[plt.gca().lines[i].set_linewidth(2) for i in range(len(plt.gca().lines))]

fig = plt.gcf(); axes = fig.gca(); fig.set_size_inches(6, 2)
axes.set_xlabel(xlabel='Aceleração [%]'); axes.set_ylabel(ylabel='Pertinência $\mu_{A}$')
plt.legend('')

print(f'Valor da Aceleração: {ControleVelocidade.output[Aceleracao.label]/100:.2%}.')