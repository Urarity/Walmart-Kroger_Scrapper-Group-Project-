
class grocery:

    def __init__(self):
        self.name = ""
        self.address1 = ""
        self.address2 = ""
        self.city = ""
        self.state = ""
        self.zipcode = ""

    def set_grocery(self, name, address1, address2, city, state, zipcode):
        self.name = name
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.zipcode = zipcode

    def set_name(self, name):
        self.name = name

    def set_address1(self, address):
        self.address1 = address

    def set_address2(self, address):
        self.address2 = address

    def set_city(self, city):
        self.city = city

    def set_state(self, state):
        self.state = state

    def set_zipcode(self, z):
        self.zipcode = z

    def get_name(self):
        return self.name

    def get_address1(self):
        return self.address1

    def get_address2(self):
        return self.address2

    def get_city(self):
        return self.city

    def get_state(self):
        return self.state

    def get_zipcode(self):
        return self.zipcode

    def display(self):
        print("Name: ", self.get_name())
        print("Address1: ", self.get_address1())
        print("Address2: ", self.get_address2())
        print("City: ", self.get_city())
        print("State: ", self.get_state())
        print("Zip code: ", self.get_zipcode())