import uuid

# Modèle représentant une tâche.
# Celle-ci est composée d'un identifiant (généré automatiquement), d'un titre et d'un status
class Task():

    def __init__(self, title):
        self.id = str(uuid.uuid4())
        self.title = title
        self.status = False