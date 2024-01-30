class Player:
    def __init__(self, name, email, chess_id, birthday, points=0):
        self.name = name
        self.email = email
        self.chess_id = chess_id
        self.birthday = birthday
        self.points = points

    def add_points(self, points):
        self.points += points

    def __str__(self):
        return (f"Name: {self.name}, Email: {self.email}\n"
                f"ID: {self.chess_id}, DoB: {self.birthday} , Points: {self.points}\n")
