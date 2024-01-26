# Urna Eletrônica
O projeto era inicialmente acadêmico, no entanto, acabei adaptando-o e tornando-o pessoal.

## Sobre o Projeto
Trata-se de uma simulação de Urna Eletrônica desenvolvida em Python que utiliza o SQLite para armazenar, em um banco de dados, informações referentes à eleição. O sistema simula um processo eleitoral, possibilitando o cadastro de eleitores, candidatos, o registro de votos e a apuração de resultados.

## Bibliotecas Utilizadas
- **sqlite3**: Biblioteca para interação com o banco de dados SQLite.
- **hashlib**: Utilizada para gerar hashes SHA-256 dos CPFs, garantindo segurança na armazenagem.
- **time**: Usada para pausar a execução em alguns pontos do programa.

## Funcionalidades
- **Cadastrar Candidatos**: Permite ao usuário registrar informações de candidatos que participarão das eleições. O sistema solicita o nome do candidato, o partido ao qual está associado, o número identificação e o cargo para o qual está concorrendo (Presidente, Governador ou Prefeito).
- **Cadastrar Eleitores**: Realiza o registro de informações sobre eleitores aptos a votar nas eleições. Ao escolher esta opção, o usuário insere o nome do eleitor, sua idade (com validação para garantir que eleitores tenham pelo menos 16 anos), o CPF (que é armazenado de forma segura usando um hash SHA-256), e o número do título de eleitor.
- **Votar**: Esta funcionalidade inicia o processo de votação. O usuário deve inserir o seu título e seu CPF corretamente, então o eleitor poderá escolher candidatos para os cargos de Presidente, Governador e Prefeito. Pode-se optar por votar em um candidato específico, escolher a opção de voto em branco ou declarar voto nulo. Branco e nulo são considerados votos inválidos e não alteram os resultados.
- **Apurar Resultados**: Exibe os nomes, partidos, números e quantidade de votos recebidos por cada candidato de cada cargo, bem como o número de votos em branco e nulos.
- **Auditoria**: Realiza uma verificação sistemática dos dados armazenados no banco de dados para garantir a integridade do processo eleitoral. A função verifica se o número total de votos registrados é consistente com o número de eleitores que votaram. Essa verificação é essencial para identificar possíveis discrepâncias ou erros no registro dos votos.

## Banco de dados
O programa utiliza um banco de dados SQLite, que é gerado quando executado e composto por três tabelas: "eleitores", "candidatos" e "inválidos". Essas tabelas armazenam todas as informações inseridas pelo usuário sobre os eleitores, candidatos, os votos recebidos por estes, e os votos inválidos (brancos e nulos).

## Pré-requisitos
Para executar este inclui a instalação do Python 3 e a disponibilidade do SQLite.

## Considerações
Com o objetivo de aprimorar ainda mais este projeto, planejo implementar uma interface gráfica utilizando a biblioteca PyQt5. Essa adição não apenas simplificará a interação com o usuário, mas também possibilitará outras melhorias e funcionalidades adicionais.

## Autor
- Vitor Arantes Vendramini - vitor_arantes@yahoo.com.br
