from movie_crud import MovieCRUD
from recommendation_system import RecommendationSystem
from movie import Movie

class CLI:
    def __init__(self):
        self.movie_crud = MovieCRUD()
        self.recommendation_system = RecommendationSystem()

    def run(self):
        while True:
            print("\n1. Criar Filme")
            print("2. Ler Filme")
            print("3. Atualizar Filme")
            print("4. Deletar Filme")
            print("5. Recomendar por Ator")
            print("6. Recomendar por Gênero")
            print("7. Recomendar por Diretor")
            print("8. Sair")
            choice = input("Escolha uma opção: ")

            if choice == "1":
                title = input("Título: ")
                genre = input("Gênero: ")
                director = input("Diretor: ")
                actors = input("Atores (separados por vírgula): ").split(",")
                self.movie_crud.create(title, genre, director, actors)
                print("Filme criado com sucesso!")

            elif choice == "2":
                title = input("Título do Filme: ")
                result = self.movie_crud.read(title)
                print(result)

            elif choice == "3":
                title = input("Título do Filme: ")
                new_title = input("Novo Título (deixe em branco para manter o mesmo): ")
                new_genre = input("Novo Gênero (deixe em branco para manter o mesmo): ")
                new_director = input("Novo Diretor (deixe em branco para manter o mesmo): ")
                new_actors = input("Novos Atores (separados por vírgula, deixe em branco para manter os mesmos): ").split(",")
                self.movie_crud.update(title, new_title, new_genre, new_director, new_actors)
                print("Filme atualizado com sucesso!")

            elif choice == "4":
                title = input("Título do Filme: ")
                self.movie_crud.delete(title)
                print("Filme deletado com sucesso!")

            elif choice == "5":
                actor_name = input("Nome do Ator: ")
                result = self.recommendation_system.recommend_by_actor(actor_name)
                print(result)

            elif choice == "6":
                genre = input("Gênero: ")
                result = self.recommendation_system.recommend_by_genre(genre)
                print(result)

            elif choice == "7":
                director_name = input("Nome do Diretor: ")
                result = self.recommendation_system.recommend_by_director(director_name)
                print(result)

            elif choice == "8":
                self.movie_crud.close()
                self.recommendation_system.close()
                break

            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    cli = CLI()
    cli.run()