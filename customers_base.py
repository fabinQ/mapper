class customer:
    def __init__(self, company, name, surname, position, mail):
        self.company = company
        self.name = name
        self.surname = surname
        self.position = position
        self.mail = mail
        self.customer_identify()

    def customer_identify(self):
        print("Name & surname: {} {}".format(self.name,self.surname))
        print("Company and position: {} {}".format(self.company, self.position))
        print("email: {}".format(self.mail))
        print()

customer_1 = customer("CompaneX sp. z.o.o", "Grzegorz", "Brzęczyszczykiewicz", "Specialist", "grzeg.brzencz@gmail.com")
customer_2 = customer("CompanDEX sp. z.o.o", "Jan", "Wiśnia", "CEO", "jan.cherry@gmail.com")
customer_3 = customer("CoDEX sp. z.o.o", "Jose", "Kowalsky", "junior", "jose.kowalsky@gmail.com")