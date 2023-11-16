import fdb
import os
import glob
import time
import sys
import getpass  # Importe a biblioteca getpass para ocultar a senha

def get_database_path():
    while True:
        database_path = input("Digite o caminho do banco de dados Firebird: ")
        if os.path.exists(database_path):
            return database_path
        else:
            print("Não foi possível encontrar o banco de dados, o caminho está incorreto. Tente novamente.")

def get_credentials():
    while True:
        user = input("Digite o nome de usuário: ")
        password = getpass.getpass("Digite a senha: ")  # Use getpass para ocultar a senha
        if check_credentials(user, password):
            return user, password
        else:
            print("Credenciais incorretas. Tente novamente.")

def check_credentials(user, password):
    return user == "SYSDBA" and password == "masterkey"

def execute_scripts(database_path, user, password, script_files):
    log_messages = []  

    try:
        
        if not check_credentials(user, password):
            print("Credenciais incorretas. Tente novamente.")
            return

       
        con = fdb.connect(
            database=database_path,
            user=user,
            password=password
        )
        print("Conexão ao banco de dados estabelecida com sucesso.")
        time.sleep(2) 

        resposta = input("Deseja iniciar a execução dos scripts? (S para sim, N para não): ").strip().lower()
        if resposta == 's':
            print("Aguarde, está sendo feita a verificação dos scripts...")
            time.sleep(3)  
        else:
            return
        
        cur = con.cursor()

        for script_file in script_files:
            file_size = os.path.getsize(script_file)
            if file_size > 2048:  
                print(f"O arquivo {os.path.basename(script_file)} é maior que 2KB. Aguarde a execução...")
                time.sleep(5)
            
            with open(script_file, 'r') as script_file:
                sql_script = script_file.read()
                try:
                    print(f"Executando script SQL: {os.path.basename(script_file.name)}")
                    cur.execute(sql_script)
                    
                    con.commit()
                    log_messages.append(f"Script {os.path.basename(script_file.name)} executado com sucesso!")
                    time.sleep(3)  
                except Exception as e:
                    con.rollback()
                    print(f"Erro ao executar o script {os.path.basename(script_file.name)}: {str(e)}")
                    log_messages.append(f"Erro ao executar o script {os.path.basename(script_file.name)}: {str(e)}")

    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {str(e)}")
        log_messages.append(f"Erro ao conectar ao banco de dados: {str(e)}")

    finally:
        
        if 'con' in locals():
            con.close()
            log_messages.append("Conexão do banco de dados encerrada.")

    
    log_dir = "log"

    
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    
    log_filename = os.path.join(log_dir, "log.txt")

    
    with open(log_filename, 'a') as log_file:
        for message in log_messages:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    if check_credentials(user, password):
        while True:
            resposta = input("Não esqueça de verificar no log se os scripts foram executados corretamente. \nDeseja encerrar o sistema? (S para sim, N para não): ").strip().lower()
            if resposta == 's':
                break
            elif resposta == 'n':
                continue
            else:
                print("Opção inválida. Responda com 'S' para sim ou 'N' para não.")

def main():
    senha_padrao = "12345"
    input("Bem-vindo, este é um sistema para rodar scripts apenas em Firebird. \nPressione Enter para continuar...")
    input("Desenvolvido pelo João, qualquer dúvida entre em contato. \nPressione Enter para continuar...")
    while True:
        senha = getpass.getpass("Digite a senha para acessar o sistema: ")
        if senha == senha_padrao:
            break
        else:
            print("Senha incorreta. Tente novamente.")

    input("ATENÇÃO !!! O EXECUTÁVEL PRECISA FICAR DENTRO DO DIRETÓRIO DOS SCRIPTS PARA FUNCIONAR CORRETAMENTE. \nPressione Enter para continuar...")

    # Selecionar o diretório do banco de dados
    database_path = get_database_path()
    
    # Configurações do banco de dados
    user, password = get_credentials()

    # Listar os arquivos .txt na pasta do executável
    script_files = glob.glob("*.txt")

    if not script_files:
        print("Nenhum arquivo de script .txt encontrado na pasta do executável.")
        return

    # Executar os scripts
    execute_scripts(database_path, user, password, script_files)

    if check_credentials(user, password):
        while True:
            resposta = input("Não esqueça de verificar no log se os scripts foram executados corretamente. \nDeseja encerrar o sistema? (S para sim, N para não): ").strip().lower()
            if resposta == 's':
                break
            elif resposta == 'n':
                continue
            else:
                print("Opção inválida. Responda com 'S' para sim ou 'N' para não.")

if __name__ == "__main__":
    main()
