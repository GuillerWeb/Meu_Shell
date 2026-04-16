# Custom Shell em Python (Sistemas Operacionais)

Este projeto consiste na implementação de um interpretador de comandos (Shell) desenvolvido para a disciplina de Sistemas Operacionais da **Universidade Federal de Mato Grosso (UFMT)**. O objetivo principal é explorar a interface entre o espaço do usuário e o Kernel do Linux através de chamadas de sistema (System Calls) POSIX.

##  Funcionalidades

O shell foi desenvolvido seguindo as restrições estritas de não utilizar bibliotecas de alto nível (como `subprocess`), focando no uso direto do módulo `os`.

- **Execução de Comandos Externos:** Suporte a comandos do sistema (ex: `ls`, `grep`, `mkdir`) com argumentos.
- **Comandos Internos (Built-ins):**
  - `cd [diretório]`: Alteração de diretório pai.
  - `pwd`: Exibe o caminho do diretório atual.
  - `exit`: Finaliza o shell.
- **Gerenciamento de Processos:**
  - Criação de processos filhos.
  - Suporte a execução em **Background** utilizando o operador `&`.
  - Sincronização entre pai e filho.

##  Tecnologias e Conceitos Utilizados

### System Calls Implementadas
Para que o Shell funcione, foram mapeadas as seguintes chamadas de sistema através do Python:

1. **`os.fork()` (clone):** Cria um novo fluxo de execução (processo filho).
2. **`os.execvp()` (execve):** Substitui a imagem do processo filho pelo programa desejado.
3. **`os.waitpid()` (wait4):** Sincroniza o processo pai, aguardando o término do filho para evitar processos zumbis.
4. **`os.chdir()` (chdir):** Altera o diretório de trabalho do processo pai.

### Fluxo de Execução
O Shell opera em um loop infinito seguindo estas etapas:
1. **Leitura:** Captura da entrada do usuário.
2. **Parsing:** Divisão do comando e seus argumentos.
3. **Análise de Contexto:** Identifica se é um comando interno ou se deve ser executado em background.
4. **Execução:** O pai faz o `fork()`, o filho executa o `execvp()` e o pai decide se aguarda (`waitpid`) ou continua o loop.

##  Análise de Depuração

O projeto inclui uma documentação técnica (PDF) com análises detalhadas utilizando as ferramentas:
- **strace:** Para monitorar a interceptação das chamadas de sistema pelo Kernel.
- **htop:** Para visualizar a hierarquia de processos (PIDs e PPIDs) e estados como **Zumbi** e **Órfão**.

## 🔧 Como Executar

1. Certifique-se de estar em um ambiente **Linux**, **WSL** ou **macOS**.
2. Clone o repositório:
   ```bash
   git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
