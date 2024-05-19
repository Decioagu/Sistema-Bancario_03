import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

# mensagem de boas vindas
apresentacao = ' SISTEMA BANCÁRIO '
print()
print(apresentacao.center(60, '*'))

# ------------------------------------------ CLASSES ------------------------------------------

# HERANÇA SIMPLES 
class Cliente: # Classe principal
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta) # retorno método das "class Saque" ou "class Deposito"

    def adicionar_conta(self, conta):
        self.contas.append(conta) # adicionar lista self.contas

# Cadastramento de Clientes
class PessoaFisica(Cliente): # Classe filha
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# HERANÇA SIMPLES
class Conta: # Classe principal
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico() # retorno classe

    @classmethod
    def nova_conta(cls, cliente, numero): 
        return cls(numero, cliente) # modifica atributos da própria classe

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    # subtrai valor do self.saldo
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\nOperação falhou! O valor informado é inválido.")

        return False

    # incrementa valor no self.saldo
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False

        return True


class ContaCorrente(Conta): # Classe filha
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\nOperação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

# HERANÇA SIMPLES
class Transacao(ABC): # Classe principal
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao): # Classe filha
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao): # Classe filha
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# -------------------------------------- FUNÇÕES AUXILIARES --------------------------------------

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    print('recuperar_conta_cliente', cliente.contas)
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return

    # não permite cliente escolher a conta
    return cliente.contas[0]

# -------------------------------------- FUNÇÕES DE EXECUÇÃO --------------------------------------


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor) # retorno classe

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor) # retorno classe

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # retorno classe
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente) # lista global

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
        return

    # retorno classe
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta) # lista global
    cliente.contas.append(conta) # lista da class Cliente

    print("\nConta criada com sucesso!")


def listar_contas(contas):
    if contas:
        for conta in contas:
            print(textwrap.dedent(str(conta)))
    else:
       print('\n Não foi encontrado nenhum conta cadastrada!')

# ----------------------------------- CORPO PRINCIPAL --------------------------------------

def main():
    clientes = []
    contas = []

    while True:
        menu = """\n
        ================ MENU ================
        [1] DEPOSITAR
        [2] SACAR
        [3] EXTRATO
        [4] CADASTRO CLIENTE
        [5] ABRIR CONTA
        [6] LISTAR CONTAS
        [7] SAIR
        """
        # exibir "menu de opções"
        print(menu)

        # entrada de parâmetro digitada pelo usuário
        opcao = input('Escolha uma opção:').lower()
        print('=' * 60)

        # FUNÇÕES DE EXECUÇÃO
        # MENU = [1] DEPOSITAR
        if opcao == "1":
            depositar(clientes)
        # MENU = [2] SACAR
        elif opcao == "2":
            sacar(clientes)
        # MENU = [3] EXTRATO
        elif opcao == "3":
            exibir_extrato(clientes)
        # MENU = [4] CADASTRO CLIENTE
        elif opcao == "4":
            criar_cliente(clientes)
        # MENU = [6] ABRIR CONTA
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        # MENU = [5] LISTAR CONTAS
        elif opcao == "6":
            listar_contas(contas)
        # MENU = [7] SAIR
        elif opcao == "7":
            break

        else:
            # caso usuário digite qualquer opção não existente no "Menu de opções" 
            print('Opção invalida, digite o NUMERO correspondente ao "MENU"')


main()
# mensagem do termino do programa
print('\nSistema finalizado com sucesso!!!\n')