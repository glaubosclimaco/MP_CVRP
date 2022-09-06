# class of locations
# class Location:
#     # id LOGRADOURO	BAIRRO	CEP	NÚMERO DE PACIENTES	endereço completo	latitude	longitude
#     def __init__(self, id, logradouro, bairro, cep, numeroPacientes, endereco, latitude, longitude):
#         self.id = id
#         self.logradouro = logradouro
#         self.bairro = bairro
#         self.cep = cep
#         self.numeroPacientes = numeroPacientes
#         self.endereco = endereco
#         self.coordenada1 = latitude
#         self.coordenada2 = longitude



# LOGRADOURO	BAIRRO	Região	CIDADE/ESTADO	CEP	NÚMERO DE PACIENTES	Coordenada1	Coordenada2

class Location:
    def __init__(self, id, logradouro, bairro, regiao, cidade, cep, numeroPacientes, latitude, longitude):
        self.id = id
        self.logradouro = logradouro
        self.bairro = bairro
        self.regiao = regiao
        self.cidade = cidade
        self.cep = cep
        self.numeroPacientes = numeroPacientes
        self.coordenada1 = latitude
        self.coordenada2 = longitude