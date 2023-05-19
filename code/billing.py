"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Created by: Luiz Quirino
Contact information: lugumar@gmail.com

"""

import boto3
import pandas as pd
import json
import configparser
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Carrega as credenciais da AWS do arquivo credentials.ini
config = configparser.ConfigParser()
config.read('credentials.ini')
aws_access_key_id = config.get('default', 'aws_access_key_id')
aws_secret_access_key = config.get('default', 'aws_secret_access_key')

# Cria a sessão do boto3 com as credenciais da AWS
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Cria o cliente do Cost Explorer
ce = session.client('ce')

# Lê o arquivo de grupos e pesos
with open('groups.json', 'r') as f:
    groups = json.load(f)
with open('weights.json', 'r') as f:
    weights = json.load(f)

# Calcula o início e o fim do último mês
end = datetime.now().replace(day=1) - relativedelta(days=1)
start = end.replace(day=1)

# Converte para string no formato necessário
start_str = start.strftime('%Y-%m-%d')
end_str = end.strftime('%Y-%m-%d')

# Faz a chamada para o Cost Explorer
response = ce.get_cost_and_usage(
    TimePeriod={
        'Start': start_str,
        'End': end_str
    },
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    GroupBy=[
        {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}
    ]
)

# Cria um DataFrame a partir da resposta
data = []
for item in response['ResultsByTime']:
    for group in item['Groups']:
        linked_account = group['Keys'][0]
        amount = float(group['Metrics']['UnblendedCost']['Amount'])
        data.append([linked_account, amount])

df = pd.DataFrame(data, columns=['LinkedAccount', 'Amount'])

# Agrupa os dados conforme os grupos definidos
grouped_data = []
for group, accounts in groups.items():
    group_sum = df[df['LinkedAccount'].isin(accounts)]['Amount'].sum()
    grouped_data.append([group, group_sum, 0])  # Adiciona uma terceira coluna para o valor fracionado

grouped_df = pd.DataFrame(grouped_data, columns=['Projeto', 'Valor em dolar', 'Valor Fracionado'])

# Aplica os pesos para as contas compartilhadas
for account, projects in weights.items():
    account_amount = df[df['LinkedAccount'] == account]['Amount'].sum()
    for project, weight in projects.items():
        project_amount = weight * account_amount
        # Encontra o índice do projeto no DataFrame
        project_index = grouped_df[grouped_df['Projeto'] == project].index[0]
        # Adiciona o valor fracionado ao total do projeto
        grouped_df.at[project_index, 'Valor em dolar'] += project_amount
        # Atualiza a coluna do valor fracionado
        grouped_df.at[project_index, 'Valor Fracionado'] += project_amount

# Escreve o DataFrame em um arquivo Excel
grouped_df.to_excel('billing_aws.xlsx', index=False)

