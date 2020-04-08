from flask_login import UserMixin

# silly user model
class User(UserMixin):
    
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def getName(self):
        return self.name

    def getPasswd(self):
        return self.password
