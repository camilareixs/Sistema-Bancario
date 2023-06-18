import json
## importando json para conseguir trabalhar melhor com os arquivos em lista 
from datetime import datetime
## importando bliblioteca de data e hora

## definindo a lista de clientes, caso já tenha clientes cadastrado, o json irá carregar o txt que transformara na lista de clientes ativas
clientes = []
with open("bancodedados.txt", "r") as arquivo:
    clientes = json.load(arquivo)
## lembrando que para funcionar a cima, caso o arquivo esteja vazio, precisa ter pelo menos "[]", assim ele identifica que clientes é uma lista

#função que recarrega os dados rescrevendo totalmente o texto pegando os dados atualizados da lista clientes 
def reloadclientes():
    with open("bancodedados.txt", "w") as arquivo:
        json.dump(clientes, arquivo)    

## mesmo metodo para gerar o extrato em arquivo
extratogeral = []
with open("bancodeextratos.txt", "r") as extrato:
    extratogeral = json.load(extrato)
print(extratogeral)
# obs precisa ao menos ter [] que seria uma lista dentro do arquivo para funcionar o json, vazio não funciona

def reloadextrato(): ## função para salvar ir salvando o extrato
    with open("bancodeextratos.txt", "w") as extrato:
        json.dump(extratogeral, extrato)    

def addextrato(cpf, tarifa, valor):
    for cliente in clientes:
        if cliente[1] == cpf:
            movimentacao = float(valor.replace("+", "").replace("-", "").replace("R$", ""))
            saldo_atual = cliente[5] - movimentacao  # Modificação: alteração do sinal para débito
            cliente[5] = saldo_atual
            break
    adicionandosaida = [databr, cpf, tarifa, valor]
    extratogeral.append(adicionandosaida)
    reloadextrato()  # Salva as alterações no arquivo "bancodeextratos.txt"


# pegando parametro de data e hora
datadehoje = datetime.now()
# formatando para o padrão br e colocando os minutos
databr = (" %s / %s / %s  %s:%.2s" % (datadehoje.day,  datadehoje.month,  datadehoje.year, datadehoje.hour, datadehoje.minute))
print(databr) 

# declarando variaveis 
operacao = 0 ## informa a operacao desejada
nome = 0 #nome do cliente
cpf = 0 #cpf do cliente
conta = 0 # tipo de conta do cliente
valor_inicial= 0 #qual o valor inicial do cliente
senha= 0 #senha do cliente
valor_deb = 0 #valor para debitar
valor_depo= 0#valor para depositar
cpf2= 0 #cpf do destinatario
valor_t=0 #valor da transferencia
apagar_cliente = 0 # usado para função apagar 
valortotal = 0 # valor total em conta
tarifa = 0 # tarifa, quando não houver é 0 
valormenosvalor = 0

### abaixo o banco pede as opções necessarias do menu ###
def opcoes():
    print("Bem Vindo ao Menu do Banco QuemPoupaTem")
    print("A seguir as operações possiveis em nosso APP")
    print("1. Novo cliente")
    print("2. Apaga cliente")
    print("3. Listar clientes")
    print("4. Débito")
    print("5. Depósito")
    print("6. Extrato")
    print("7. Transferência entre contas")
    print("8. Doação")
    print("9. Sair")
    global operacao
    operacao = int(input("Digite a opção desejada: "))

### funcao para cadastrar novos clientes ###
def novo_cliente():
## comeca a pedir informacoes ##
    nome = input("Digite seu nome: ")
    cpf = input("Digite seu CPF: ")
    conta = input("Sua conta vai ser comum ou plus?: ")
    valor_inicial= float(input("Valor inicial: "))
    senha= input("Digite a sua senha: ")
## termina de pedir informacoes ##
    valortotal = valor_inicial  
    cliente = [nome, cpf,conta,valor_inicial, senha, valortotal] #a lita esta gaurdando as inofrmaçoes coorrelacionando uma string com uma variavel
    #inofrmacoes coorrelacionando uma string com uma variavel
    clientes.append(cliente) #esta colocando o novo valor na lista
    operacaoextrato = (" - %f" % valortotal)
    addextrato(cpf,tarifa,operacaoextrato)
    reloadclientes()
    print("Cliente cadastrado com sucesso.")
    print(nome,cpf,conta,valortotal,senha)

## funcao para apagar um cliente ##
def apaga_cliente():
    ## comeca a pedir informacoes ##
    print("Você escolheu a opção apagar cliente") 
    cpf = input("Digite o CPF do cliente que deseja apagar: ") # pede o CPF para deletar do sistema
    for x in range(len(clientes)): # anda pelos clientes até com a range até o final da lista
        ## termina de pedir informacoes ##
        for a in clientes: 
            if cpf == a[1]: #localiza o cpf e exlui do sistema
                print(clientes)
                clientes.pop(x)
                print("Cliente apagado com sucesso.")
                print(clientes)
                reloadclientes()
                   
### funcao que lista todos os clientes ###
def listar_clientes():
    print("Você escolheu a opção listar clientes")
    for x in clientes: #confere os clientes dentro da lista
            print("Nome:", x[0]) #as quatro linhas abaixo assim como essa imprime as informcoes buscando todas existentes no lista de clientes
            print("CPF:", x[1])
            print("Conta:", x[2])
            print("Saldo Atual:", x[5])
            print("Senha:", x[4])
            print("Fim da lista de clientes.")

### funcao para debitar ###
def debito():
    print("Você escolheu a opção débito")
    cpf = input("Digite seu CPF: ")
    senha = input("Digite a sua senha: ")
    valordebitado = float(input("Qual valor deseja debitar?: "))
    for x in clientes:
        for j in x:
            if (j == senha and cpf == x[1]) and x[2] == "plus":
                print("Encontramos o seu cadastro, cliente PLUS tem direito especial, somente 3 por cento de taxa")
                tarifa = valordebitado * 0.03
                valorconfere = x[5] - (valordebitado + tarifa)
                if valorconfere > -5000:
                    x[5] = valorconfere
                    print("Transação feita, seu saldo é de R$%.2f" % x[5])
                    valor = tarifa + valordebitado
                    valor = "-R$%.2f" % valor
                    addextrato(x[1], tarifa, valor)
                    reloadclientes()
                    tarifa = 0
                else:
                    print("saldo insuficiente deposite para continuar")
                    tarifa = 0
            if (j == senha and cpf == x[1]) and x[2] == "comum":
                print("Encontramos o seu cadastro, cliente comum tem possui 5 por cento de taxa, vire plus e pague somente 3 por cento")
                tarifa = valordebitado * 0.05
                valorconfere = x[5] - (valordebitado + tarifa)
                if valorconfere > -1000:
                    x[5] = valorconfere
                    print("Transação feita, seu saldo é de R$%.2f" % x[5])
                    valor = tarifa + valordebitado
                    valor = "-R$%.2f" % valor
                    addextrato(x[1], tarifa, valor)
                    reloadclientes()
                    tarifa = 0
                else:
                    print("saldo insuficiente deposite para continuar")
                    tarifa = 0

## função deposito bancario 
def valor_cliente():
    print("Você escolheu deposito bancario")
    cpf = input("Digite seu CPF: ")
    for x in clientes:      
        if x[1] == cpf:#confere se o cpf existe/esta correto
            valor_depo= float(input("Digite o valor a ser depositado: ")) ## valor a ser depositado
            annterior = x[5] ## declarando para informar na frase o saldo antigo
            x[5] += (valor_depo) # soma o valor depositado com saldo anterior 
            reloadclientes() # recarrega a lista clientes
            print("O valor de R$", valor_depo, " foi depositado com sucesso. Saldo anterior: ", annterior,"saldo atual: ", x[5])          
            valor = ("+R$%.2f" % (valor_depo))
            addextrato(x[1],tarifa,valor)
            return
    print("CPF inexistente") # caso nenhum cliente seja achado com cpf informado, for encerra com a informação


### funcao transferencia ###
def transferencia():
    print("Você escolheu transferência") ## informa a pagina que entrou
    cpf = input("Digite seu CPF: ") #CPF DA PESSOA QUE IRÁ TRANSFERIR
    senha = input("Digite a sua senha: ") # SENHA DA PESSOA QUE IRÁ TRANSFERIR
    destinatario = input("Digite o CPF/CNPJ do destinatario: ") # CPF DA CONTA DE DESTINO
    valor_t = float(input("Digite o valor da transferência: ")) # VALOR DA TRANSFERENCIA
    for x in clientes: # FOR PARA INTERAR SOBRE OS CLIENTES
        if (x[4] == senha and cpf == x[1]): # CONFERINDO CADA SENHA E CPF, DANDO MATCH, PROSSEGUE 
            novosaldo = x[5] - valor_t # JA DEFINIMOS O PROVAVEL NOVO SALDO
            if (x[2] == "comum")  and (novosaldo < -1000): #CONFERENCIA SE ESTÁ NO LIMITE DISPONIVEL 
                print("Saldo insuficiente") 
            elif (x[2] == "plus") and (novosaldo < -5000): #CONFERENCIA SE ESTÁ NO LIMITE DISPONIVEL 
                print("Saldo insuficiente")
            elif (x[2] == "comum")  and (novosaldo > -1000): # VERIFICA QUE O LIMITE ESTÁ DISPONIVEL CONTA COMUM 
                print("Credênciais corretas")
                for destino in clientes: # MAIS UMA INTERAÇÃO SOBRE OS CLIENTES PARA ACHAR O DESTINATARIO
                    if (destino[1] == destinatario): # CONFERINDO AS CREDENCIAIS                   
                        x[5] -= valor_t # RETIRANDO O SALDO DA CONTA DO REMETENTE 
                        destino[5] += valor_t # DEPOSITANDO NA CONTA DO DESTINATARIO
                        valor = ("+R$%.2f" % (valor_t))
                        addextrato(destino[1],tarifa,valor) 
                        valor = ("-R$%.2f" % (valor_t))    ##     adicionando dados no extrato de ambos
                        addextrato(x[1],tarifa,valor) 
                        reloadclientes() # SALVANDO 
                    else:
                        print("Operação falha, tente novamente mais tarde") # ALGO DEU ERRADO, CPF, SENHA, VALOR
            elif (x[2] == "plus") and (novosaldo > -5000): # ## A MESMA SEQUÊNCIA DO CÓDIGO A CIMA, SÓ MUDA O TIPO DE CONTA "PLUS"
                print("Credênciais corretas")
                for destino in clientes:
                    if (destino[1] == destinatario):
                        novosaldo = destino[5] + valor_t
                        x[5] -= valor_t
                        destino[5] += valor_t
                        valor = ("+R$%.2f" % (valor_t))
                        addextrato(destino[1],tarifa,valor) 
                        valor = ("-R$%.2f" % (valor_t))    ##     adicionando dados no extrato de ambos
                        addextrato(x[1],tarifa,valor) 
                        reloadclientes()
                    else:
                        print("Operação falha, tente novamente mais tarde")
            else:
                    print("Erro cadastral, entre em contato para atualização de cadastro")


def extrato():
    print("Você escolheu extrato")
    cpf = input("Digite seu CPF: ")
    senha = input("Digite a sua senha: ")
    cliente_encontrado = False
    for x in clientes:
        if x[1] == cpf and x[4] == senha:  # Verifica se o CPF e senha correspondem a um cliente
            cliente_encontrado = True  # Define a variável cliente_encontrado como True para indicar que o cliente foi encontrado
            valorconfere = x[5]  # Armazena o saldo do cliente encontrado
            print("Cliente:", x[0])  # Exibe o nome do cliente
            print("CPF:", x[1])  # Exibe o CPF do cliente
            print("Conta:", x[2])  # Exibe o número da conta do cliente
            break  # Interrompe o loop, uma vez que o cliente foi encontrado
    if cliente_encontrado:
        for j in extratogeral:
            if cpf == j[1]:
                movimentacao = float(j[3].replace("+", "").replace("-", "").replace("R$", "")) # remova o sinal "+", "-", e "R$"
                sinal = "+" if j[3].startswith("+") else "-"
                print("Data: ", j[0], end=" ")
                print("Movimentação: ", sinal + str(movimentacao), end=" ")
                print("Tarifa: ", j[2], end=" ")
                print(" Saldo: ", valorconfere)
                print()  # Adiciona uma linha em branco entre cada transação
    else:
        print("Cliente não encontrado ou senha incorreta")

instituicoes = ["AACD", "Teleton", "Criança esperança"]
#### funcao de doacao ####
def doacao():
    print("Você escolheu doação")
    cpf = input("Digite seu CPF: ")
    for cliente in clientes:
        if cliente[1] == cpf:
            instituicao = input("Escolha a instituição (AACD, Teleton, Criança esperança): ")
            if instituicao in instituicoes:
                valor_doacao = float(input("Digite o valor: "))
                
                if ((cliente[2] == "comum") and (cliente[5] - valor_doacao < -1000)) or ((cliente[2] == "plus") and (cliente[5] - valor_doacao < -5000)):
                    print("Saldo insuficiente.")
                else:
                    cliente[5] -= valor_doacao
                    print("Doação para", instituicao, "feita com sucesso.")
                    valor = ("-R$%.2f" % valor_doacao)
                    addextrato(cliente[1], tarifa, valor)
                    reloadclientes()
                    return
            else:
                print("Instituição não encontrada.")
                return
    print("CPF inexistente.")


#### laço de repetição do menu principal ####
while True:
    opcoes()
    print(operacao)
    if operacao == 1: ## if elif e else verifica a opção no menu
        novo_cliente()
    elif operacao == 2:
        apaga_cliente()
    elif operacao == 3:
        listar_clientes()
    elif operacao == 4:
        debito()
    elif operacao == 5:
        valor_cliente()
    elif operacao == 6:
        extrato()
    elif operacao == 7:
        transferencia()
    elif operacao == 8:
        doacao()
    elif operacao == 9: ## paralisa o app
        print("Que pena que escolheu sair, esperamos você em breve")
        break
    else:
        print("Operação invalida")