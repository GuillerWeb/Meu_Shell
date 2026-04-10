import os
import sys

def main():
    print("---Bem-vindo ao GSP Shell--- \n")

    while True:
        try:
            # Exibir o prompt e ler a entrada do usuário
            user_input = input("gsp-shell> ").strip()

        except EOFError:
            # Captura o Ctrl+D (Fim de arquivo) para sair graciosamente
            print("\nEncerrando o shell...")
            break
        except KeyboardInterrupt:
            # Captura o Ctrl+C para não matar o shell acidentalmente
            print()
            continue

        # Ignora linhas em branco (se o usuário só apertou Enter)
        if not user_input:
            continue

        # ==========================================================
        # 1. Fazer o parse (separação) da linha de comando
        # ==========================================================

        elementos = user_input.split()      # split () devolve uma lista e organiza as strings
        comando_principal = elementos[0]    # separa a 1 posição da lista para ser o comando
        argumentos = elementos[1:]          # as demais posições todas seram argumentos

        # ==========================================================
        # 2. Verifica se é execução em background (se termina com '&')
        # ==========================================================

        
        background = False
        if argumentos and argumentos[-1] == '&':    # condição para detectar o & no final da lista de argumentos
            background = True                       # background ativo, assim processo pai não precisa esperar filho
            argumentos = argumentos[:-1]            # remove o '&' da lista de argumentos para não afetar o método execvp()
            
        elif comando_principal == '&':   # caso o usuário digitou só '&'
            continue

        # ==========================================================
        # 3. Tratar comandos internos (Built-ins) ANTES do fork
        # ==========================================================

        if comando_principal == "exit":
            print("Shell encerrado...")
            break

        elif comando_principal == "cd":

            try:
                if len(argumentos) > 0:
                    destino = argumentos[0]
                else:
                    destino = os.path.expanduser("~")  # caso digite apenas o cd sem argumento retorna ao diretório home

                os.chdir(destino)                      # esse método que faz a troca de diretório dentro do kernel via system call
                
            except FileNotFoundError:
                print(f"cd: Arquivo ou diretório não encontrado: {destino}")
            except PermissionError:
                print(f"cd: permissão negada: {destino}")
            continue  

        elif comando_principal == "pwd":
            print(os.getcwd())  # método que por meio do SO olha o PCB e retorna o diretório atual
            continue

        # ==========================================================
        # 4. Criar processo filho e executar comando externo
        # ==========================================================
        try:

            pid = os.fork()  # vai gerar novos processos clones(filhos)

            if pid == 0:
                # --- CÓDIGO DO PROCESSO FILHO ---
                try:
                    # os.execvp substitui um processo atual por um novo
                    # primeiro parametro seria a localização do binário do meu comando
                    # segundo parametro mostraria o comando e os argumentos usados
                    os.execvp(comando_principal, [comando_principal] + argumentos)                    
                
                except FileNotFoundError:
                    print(f"gsp-shell: comando não encontrado: {comando_principal}",file=sys.stderr,)
                    continue

            elif pid > 0:
                # --- CÓDIGO DO PROCESSO PAI (SHELL) ---
                if background:
                    print(f"[processo em background] PID={pid}") # não espera o processo filho e volta ao loop imediatamente
                    
                    
                else:
                    os.waitpid(pid, 0)  # espera o processo filho terminar
                

            else:
                print("Erro ao criar processo filho.")

        except OSError as e:
            print(f"Erro do sistema operacional: {e}")


if __name__ == "__main__":
    main()
