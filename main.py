'''
    Padrao de Projeto PubSub

    Video aula passada por: Eduardo Mendes
    Fonte: https://www.youtube.com/watch?v=sbCJucr8aJg
    (Copia dos codigos dos slides exibidos)

'''


class Publicador:
    # Pub_Sub aqui seriam os lugares onde publicar (facebook, email, sms, twiter...)
    def __init__(self, topico, pub_sub):
        self.topico = topico
        self.mensagens = []
        self.pub = pub_sub

    # Publica as mensagens na lista do PUBLICADOR (roteador)
    # Perceba q é passado apenas a mensagem como parametro,
    # o topico e lugar (pub_sub) ficam gravados na criacao deste objeto
    def publicar(self, mensagem):
        msg = {'topico': self.topico, 'mensagem': mensagem}
        self.pub.receber_mensagem(msg)


# Guarda os dados do inscrito E qual acao ele deseja do roteador
class Inscrito:
    def __init__(self, nome):
        self.nome = nome

    # Executa a acao que o inscrito deseja (receber email, SMS, ZAP...)
    def atualizar(self, topico, mensagem):
        print(f'|{topico}|\t{self.nome}\trecebeu: {mensagem}')


# Classe Roteadora (lista de email, facebook, twiter, linkedin...)
class PubSub:
    # Ele guarda:
    #   Topicos + Inscritos
    #   As publicacoes recebidas
    def __init__(self):
        self.inscrito_topico = {}
        self.fila_mensagens: list(dict(str, str)) = []

    # O publicador tem um dicionario = TOPICOS: INSCRITOS
    # O usuario vai adicionando os INSCRITOS (classes) em seus TOPICOS
    # Se o TOPICO nao existir, é adicionada uma entrada no dicionario
    # com o TOPICO e os INSCRITOS (classe)
    #
    # OBS.: a variavel self.inscrito_topico[topico].add(inscrito)
    # tera essa aparencia, por exemplo:
    # {
    # 'Esporte': {
    #     <__main__.Inscrito at 0x21916bfcb88>,
    #     <__main__.Inscrito at 0x21916bfcc88>},
    # 'Economia': {
    #     <__main__.Inscrito at 0x21916bfcd08>},
    # 'TV': {
    #     <__main__.Inscrito at 0x21916bfcb88>}
    # }
    def adicionar_inscrito(self, topico, inscrito):
        if topico in self.inscrito_topico:
            self.inscrito_topico[topico].add(inscrito)
        else:
            self.inscrito_topico[topico] = {inscrito}

    # Recebe as mensagens vindas dos publicadores
    # Tem essa aparencia:
    # [
    #   {'topico': 'Economia',  'mensagem': 'Alta do dolar incomoda turistas'},
    #   {'topico': 'Economia',  'mensagem': 'Queda do indice Bovespa'},
    #   {'topico': 'Esporte',   'mensagem': 'Jogo cancelado devido ao mau tempo'},
    #   {'topico': 'TV',        'mensagem': 'Novo filme em cartaz'}
    # ]
    def receber_mensagem(self, mensagem):
        self.fila_mensagens.append(mensagem)

    # Pega cada item guardado no dicionario de INSCRITO_TOPICO
    # e executa o metodo ATUALIZAR (este poderia acionar o envio
    # de SMS, publicacao no Zap, LinkedIn...)
    def enviar_mensagem(self, topico, mensagem):
        for inscrito in self.inscrito_topico[topico]:
            inscrito.atualizar(topico, mensagem)

    # Se houver publicacoes novas na FILA_MENSAGENS,
    # aciona o metodo enviar_mensagem
    def broadcast(self):
        for msg in self.fila_mensagens:
            self.enviar_mensagem(msg['topico'], msg['mensagem'])

        self.fila_mensagens = []


# Criacao do objetos
edu = Inscrito('Eduardo')
mar = Inscrito('Maria')
jos = Inscrito('Jose')
mur = Inscrito('Murilo')

bus = PubSub()

blog_economia = Publicador('Economia', bus)
blog_esporte = Publicador('Esporte', bus)
blog_tv = Publicador('TV', bus)

# Configuracao dos objetos
bus.adicionar_inscrito('Esporte', edu)
bus.adicionar_inscrito('Esporte', mar)
bus.adicionar_inscrito('Economia', jos)
bus.adicionar_inscrito('TV', edu)

blog_economia.publicar('Alta do dolar incomoda turistas')
blog_economia.publicar('Queda do indice Bovespa')
blog_esporte.publicar('Jogo cancelado devido ao mau tempo')

# Distribuir as msg´s
bus.broadcast()

print('\nAguardando nova lista de publicacao...')

blog_tv.publicar('Novo filme em cartaz')
bus.broadcast()
