# class of locations
class Location:
    # id LOGRADOURO	BAIRRO	CEP	NÚMERO DE PACIENTES	endereço completo	latitude	longitude
    def __init__(self, id, logradouro, bairro, cep, numeroPacientes, endereco, latitude, longitude):
        self.id = id
        self.logradouro = logradouro
        self.bairro = bairro
        self.cep = cep
        self.numeroPacientes = numeroPacientes
        self.endereco = endereco
        self.coordenada1 = latitude
        self.coordenada2 = longitude

