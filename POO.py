class Cachorros:   
    def __init__(self, cor_de_pelo, tamanho, idade, nome):
        self.cor_de_pelo = cor_de_pelo
        self.tamanho = tamanho
        self.idade = idade
        self.nome = nome

    def latir(self):
        print(f'{self.nome} disse au au')

    def correr(self):
        print(self.nome +' esta correndo')

cachorro_1 = Cachorros('preto',10,'20','Jasmim')

print(cachorro_1.nome)
print(cachorro_1.cor_de_pelo)
print(cachorro_1.tamanho)
cachorro_1.tamanho = 15
print(cachorro_1.tamanho)

cachorro_1.latir()

cachorro_1.correr()