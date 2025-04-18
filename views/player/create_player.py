class CreatePlayerView:
    @staticmethod
    def display_add_player_form():
        print("""
==================================================
\u265d  Add New Player   \u2657 :
==================================================
""")

        first_name = input("First name : ")
        last_name = input("Last Name : ")
        birthdate = input("Birthdate (DD-MM-YYYY) : ")
        chess_id = input("Chess ID (2 letters + 5 digits) : ")
        return first_name, last_name, birthdate, chess_id
