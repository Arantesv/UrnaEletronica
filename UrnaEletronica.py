import sqlite3
import hashlib
import time

banco_dados = sqlite3.connect("urna_eletronica.db")
cursor = banco_dados.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS eleitores (nome TEXT NOT NULL, idade INTEGER NOT NULL, cpf TEXT UNIQUE NOT NULL, titulo INTEGER UNIQUE NOT NULL, votou INTEGER NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS candidatos (nome TEXT NOT NULL, partido TEXT NOT NULL, numero INTEGER NOT NULL, cargo TEXT NOT NULL, votos INTEGER NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS invalidos (brancos INTEGER, nulos INTEGER, cargo TEXT UNIQUE NOT NULL)")
cursor.execute("INSERT OR IGNORE INTO invalidos VALUES (0, 0, 'Presidente')")
cursor.execute("INSERT OR IGNORE INTO invalidos VALUES (0, 0, 'Governador')")
cursor.execute("INSERT OR IGNORE INTO invalidos VALUES (0, 0, 'Prefeito')")
banco_dados.commit()

def cadastrar_eleitor(nome, idade, cpf, titulo):
    cpf_hash = hashlib.sha256(cpf.encode()).hexdigest()
    cursor.execute("INSERT INTO eleitores VALUES (?, ?, ?, ?, 0)", (nome, idade, cpf_hash, titulo))
    banco_dados.commit()

def cadastrar_candidato(nome, partido, numero, cargo):
    cursor.execute("INSERT INTO candidatos VALUES (?, ?, ?, ?, 0)", (nome, partido, numero, cargo))
    banco_dados.commit()
    
def voto_realizado(titulo):
    cursor.execute("UPDATE eleitores SET votou = 1 WHERE titulo = ?", (titulo,))
    banco_dados.commit()

def inserir_voto(numero_candidato, cargo):
    cursor.execute("UPDATE candidatos SET votos = votos + 1 WHERE numero = ? AND cargo = ?", (numero_candidato, cargo,))
    banco_dados.commit()

def inserir_branco(cargo):
    cursor.execute("UPDATE invalidos SET brancos = brancos + 1 WHERE cargo = ?", (cargo,))
    banco_dados.commit()

def inserir_nulo(cargo):
    cursor.execute("UPDATE invalidos SET nulos = nulos + 1 WHERE cargo = ?", (cargo,))
    banco_dados.commit()

def autenticacao(titulo, cpf):
    cpf_hash = hashlib.sha256(cpf.encode()).hexdigest()
    cursor.execute("SELECT * FROM eleitores WHERE titulo = ? AND cpf = ?", (titulo, cpf_hash))
    return cursor.fetchone()

def verificar_candidato(numero, cargo):
    cursor.execute("SELECT nome, partido, cargo FROM candidatos WHERE numero = ? AND cargo = ?", (numero, cargo,))
    return cursor.fetchone()

def eleitor_votou(titulo):
    cursor.execute("SELECT votou FROM eleitores WHERE titulo = ?", (titulo,))
    result = cursor.fetchone()
    return result [0]

def votar(cargo):
    while True:
        candidato = input(f"Digite o número do candidato que deseja votar para {cargo}: ")
        if candidato.lower() == 'branco':
            confirmacao = input(f"Você confirma o seu voto em BRANCO para {cargo}? ")
            if confirmacao.lower() == 'sim':
                print("Voto em branco registrado com sucesso!")
                inserir_branco(cargo)
                break 
            else:
                print("Voto não confirmado. Por favor, digite novamente.")
        else:
            candidato_info = verificar_candidato(candidato, cargo)    
            if candidato_info:
                confirmacao = input(f"Você confirma o seu voto no {candidato_info[0]} do partido {candidato_info[1]} para {candidato_info[2]}? ")
                if confirmacao.lower() == 'sim':
                    print("Voto registrado com sucesso!")
                    inserir_voto(candidato, cargo)
                    break 
                else:
                    print("Voto não confirmado. Por favor, digite novamente.")
            else:
                confirmacao = input(f"Não foi encontrado nenhum candidato com o número {candidato}. Você deseja votar NULO para {cargo}? ")
                if confirmacao.lower() == 'sim':
                    print("Voto nulo registrado com sucesso!")
                    inserir_nulo(cargo)
                    break 
                else:
                    print("Voto não confirmado. Por favor, digite novamente.")

def votacao(eleitor):
    cargos = ["Presidente", "Governador", "Prefeito"]
    for cargo in cargos:
        votar(cargo)
    voto_realizado(eleitor)

def auditoria():
    print("\nContabilizando votos e checando dados...")

    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE votou = 1")
    total_votos = cursor.fetchone()[0] * 3

    cursor.execute("SELECT SUM(votos) FROM candidatos WHERE cargo = 'Presidente'")
    votos_presidente = cursor.fetchone()[0]
    votos_presidente = votos_presidente if votos_presidente is not None else 0

    cursor.execute("SELECT SUM(votos) FROM candidatos WHERE cargo = 'Governador'")
    votos_governador = cursor.fetchone()[0]
    votos_governador = votos_governador if votos_governador is not None else 0

    cursor.execute("SELECT SUM(votos) FROM candidatos WHERE cargo = 'Prefeito'")
    votos_prefeito = cursor.fetchone()[0]
    votos_prefeito = votos_prefeito if votos_prefeito is not None else 0

    cursor.execute("SELECT brancos, nulos FROM invalidos WHERE cargo = 'Presidente'")
    votos_brancos_presidente, votos_nulos_presidente = cursor.fetchone()

    cursor.execute("SELECT brancos, nulos FROM invalidos WHERE cargo = 'Governador'")
    votos_brancos_governador, votos_nulos_governador = cursor.fetchone()

    cursor.execute("SELECT brancos, nulos FROM invalidos WHERE cargo = 'Prefeito'")
    votos_brancos_prefeito, votos_nulos_prefeito = cursor.fetchone()

    time.sleep(2)    

    if (total_votos == votos_presidente + votos_governador + votos_prefeito +
        votos_brancos_presidente + votos_nulos_presidente +
        votos_brancos_governador + votos_nulos_governador +
        votos_brancos_prefeito + votos_nulos_prefeito
        ):
        print("Votação Auditada! Todos os votos foram contabilizados corretamente.")
    else:
        print("Erro na Auditoria! A quantidade de pessoas que votaram não está de acordo com o total de votos.")

def resultados_eleicao(cargo):
    cursor.execute(f"SELECT nome, partido, numero, votos FROM candidatos WHERE cargo = ? ORDER BY votos DESC", (cargo,))
    resultados_candidatos = cursor.fetchall()

    cursor.execute("SELECT brancos, nulos FROM invalidos WHERE cargo = ?", (cargo,))
    resultados_invalidos = cursor.fetchone()

    total_votos_validos = sum(candidato[3] for candidato in resultados_candidatos)
    total_votos = total_votos_validos + resultados_invalidos[0] + resultados_invalidos[1]

    porcentagem_brancos = (resultados_invalidos[0] / total_votos) * 100
    porcentagem_nulos = (resultados_invalidos[1] / total_votos) * 100

    print(f"\nResultados da eleição para o cargo de {cargo}: \n")

    print("{:<20} {:<15} {:<10} {:<10}".format("Nome", "Partido", "Número", "Votos"))
    print("-" * 55)
    for candidato in resultados_candidatos:
        print("{:<20} {:<15} {:<10} {:<10}".format(candidato[0], candidato[1], candidato[2], candidato[3]))
    print("-" * 55)

    print(f"\nTotal de votos: {total_votos}")
    print(f"Total de votos válidos: {total_votos_validos} ({(total_votos_validos / total_votos) * 100:.1f}% do total)")
    print(f"Voto(s) em branco: {resultados_invalidos[0]} ({porcentagem_brancos:.1f}% do total)")
    print(f"Voto(s) nulo(s): {resultados_invalidos[1]} ({porcentagem_nulos:.1f}% do total)")

def main():
    while True:
        print("\n+++++++ MENU - URNA ELETRÔNICA +++++++\n")
        print("1. Cadastrar Candidatos")
        print("2. Cadastrar Eleitores")
        print("3. Votar")
        print("4. Apurar Resultados")
        print("5. Auditoria")
        print("6. Encerrar")
        opcao = int(input("\nOpção escolhida: "))

        if opcao == 1:
            nome = input("Digite o nome do Candidato: ")
            partido = input("Digite o partido: ")
            numero = int(input("Digite o número: "))
            cargo = input("Digite o cargo (Presidente, Governador ou Prefeito): ")
            cargos_permitidos = ["Presidente", "Governador", "Prefeito"]
            if cargo in cargos_permitidos:
                cadastrar_candidato(nome, partido, numero, cargo)
                print(f"\n{nome} - {numero} do partido {partido} cadastrado com sucesso para as eleições de {cargo}.")
                time.sleep(2)
            else:
                print("\nCargo inválido. Por favor, digite novamente.")
                time.sleep(2)

        elif opcao == 2:
            nome = input("Digite o nome do Eleitor: ")
            idade = int(input("Digite a idade: "))
            if idade < 16:
                print("\nNão é permitido votar com menos de 16 anos.")
            else:                            
                cpf = input("Digite o CPF: ")
                titulo = int(input("Digite o número do título de eleitor: "))
                cadastrar_eleitor(nome, idade, cpf, titulo)
                print(f"\n{nome}; {idade} anos; CPF: {cpf}; Título: {titulo}; cadastrado com sucesso no banco de dados dos eleitores.")
                time.sleep(2)
        
        elif opcao == 3:
            cpf = input("Digite o seu CPF (apenas número): ")
            titulo_eleitor = int(input("Digite o seu título de eleitor: "))
            
            resultado_autenticacao = autenticacao(titulo_eleitor, cpf)
            if resultado_autenticacao:
                print("\nAutenticação bem-sucedida.")
                time.sleep(2)
                if eleitor_votou(titulo_eleitor) == 0:                    
                    votacao(titulo_eleitor)
                else:
                    print("Não é permitido votar mais de uma vez.")
            else:
                print("\nFalha na autenticação. Eleitor não encontrado ou dados incorretos.")
                time.sleep(2)

        elif opcao == 4:
            cargos = ["Presidente", "Governador", "Prefeito"]
            for cargo in cargos:
                resultados_eleicao(cargo)
                input("\nPressione ENTER para continuar...")

        
        elif opcao == 5:
            auditoria()
            input("\nPressione ENTER para voltar ao menu...")
                        
        elif opcao == 6:
            break

        else:
            print("\nOpção inválida, por favor digite novamente entre as opções 1 e 6.")
            time.sleep(2)

    banco_dados.close()

if __name__ == "__main__":
    main()
