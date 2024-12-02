from movie_crud import MovieCRUD
from recommendation_system import RecommendationSystem
from user_crud import UserCRUD
from review_crud import ReviewCRUD
from movie import Movie
from user import User
from review import Review

class CLI:
    def __init__(self):
        self.movie_crud = MovieCRUD()
        self.recommendation_system = RecommendationSystem()
        self.user_crud = UserCRUD()
        self.review_crud = ReviewCRUD()

    def run(self):
        while True:
            print("\n1. Criar Filme")
            print("2. Ler Filme")
            print("3. Atualizar Filme")
            print("4. Deletar Filme")
            print("5. Recomendar por Ator")
            print("6. Recomendar por Gênero")
            print("7. Recomendar por Diretor")
            print("8. Criar Usuário")
            print("9. Ler Usuário")
            print("10. Atualizar Usuário")
            print("11. Deletar Usuário")
            print("12. Criar Avaliação")
            print("13. Ler Avaliação")
            print("14. Atualizar Avaliação")
            print("15. Deletar Avaliação")
            print("16. Recomendar Filmes por Nota")
            print("17. Sair")
            choice = input("Escolha uma opção: ")

            if choice == "1":
                title = input("Título: ")
                genre = input("Gênero: ")
                director = input("Diretor: ")
                actors = input("Atores (separados por vírgula): ").split(",")
                filme = Movie(title, genre, director, actors)
                self.movie_crud.create(filme)
                print("Filme criado com sucesso!")

            elif choice == "2":
                title = input("Título do Filme: ")
                result = self.movie_crud.read(title)
                if result:
                    print(result)
                else:
                    print("Filme não encontrado.")

            elif choice == "3":
                title = input("Título do Filme: ")
                new_title = input("Novo Título (deixe em branco para manter o mesmo): ") or None
                new_genre = input("Novo Gênero (deixe em branco para manter o mesmo): ") or None
                new_director = input("Novo Diretor (deixe em branco para manter o mesmo): ") or None
                new_actors = input("Novos Atores (separados por vírgula, deixe em branco para manter os mesmos): ")
                new_actors = new_actors.split(",") if new_actors else None

                # Criação de um objeto Movie com os dados atualizados
                updated_movie = Movie(
                    title=new_title,
                    genre=new_genre,
                    director=new_director,
                    actors=new_actors
                )

                self.movie_crud.update(title, updated_movie)
                print("Filme atualizado com sucesso!")

            elif choice == "4":
                title = input("Título do Filme: ")
                self.movie_crud.delete(title)
                print("Filme deletado com sucesso!")

            elif choice == "5":
                actor_name = input("Nome do Ator: ")
                result = self.recommendation_system.recommend_by_actor(actor_name)
                if isinstance(result, list):
                    for recommendation in result:
                        print(recommendation)
                else:
                    print(result)

            elif choice == "6":
                genre = input("Gênero: ")
                result = self.recommendation_system.recommend_by_genre(genre)
                if result:
                    for record in result:
                        print(f"Título: {record['title']}, Gênero: {record['genre']}, Diretor: {record['director']}")
                else:
                    print(f"Nenhum filme encontrado para o gênero: {genre}")

            elif choice == "7":
                director_name = input("Nome do Diretor: ")
                result = self.recommendation_system.recommend_by_director(director_name)
                if result:
                    for record in result:
                        print(f"Título: {record['title']}, Gênero: {record['genre']}, Diretor: {record['director']}")
                else:
                    print(f"Nenhum filme encontrado para o diretor: {director_name}")

            elif choice == "8":
                username = input("Nome do Usuário: ")
                user = User(username)
                self.user_crud.create(user)
                print("Usuário criado com sucesso!")

            elif choice == "9":
                username = input("Nome do Usuário: ")
                result = self.user_crud.read(username)
                if result:
                    print(result)
                else:
                    print("Usuário não encontrado.")

            elif choice == "10":
                username = input("Nome do Usuário: ")
                new_username = input("Novo Nome do Usuário (deixe em branco para manter o mesmo): ") or None
                updated_user = User(new_username)
                self.user_crud.update(username, updated_user)
                print("Usuário atualizado com sucesso!")

            elif choice == "11":
                username = input("Nome do Usuário: ")
                self.user_crud.delete(username)
                print("Usuário deletado com sucesso!")

            elif choice == "12":
                username = input("Nome do Usuário: ")
                movie_title = input("Título do Filme: ")
                rating = input("Avaliação (1-5): ")
                review_text = input("Comentário: ")
                review = Review(username, movie_title, rating, review_text)
                self.review_crud.create(review)
                print("Avaliação criada com sucesso!")

            elif choice == "13":
                username = input("Nome do Usuário: ")
                movie_title = input("Título do Filme: ")
                result = self.review_crud.read(username, movie_title)
                if result:
                    print(result)
                else:
                    print("Avaliação não encontrada.")

            elif choice == "14":
                username = input("Nome do Usuário: ")
                movie_title = input("Título do Filme: ")
                new_rating = input("Nova Avaliação (1-5): ")
                new_review_text = input("Novo Comentário: ")
                updated_review = Review(username, movie_title, new_rating, new_review_text)
                self.review_crud.update(username, movie_title, updated_review)
                print("Avaliação atualizada com sucesso!")

            elif choice == "15":
                username = input("Nome do Usuário: ")
                movie_title = input("Título do Filme: ")
                self.review_crud.delete(username, movie_title)
                print("Avaliação deletada com sucesso!")

            elif choice == "16":
                result = self.recommendation_system.recommend_by_rating()
                if isinstance(result, list):
                    for recommendation in result:
                        print(recommendation)
                else:
                    print(result)


            elif choice == "17":
                self.movie_crud.close()
                self.recommendation_system.close()
                self.user_crud.close()
                self.review_crud.close()
                break

            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    cli = CLI()
    cli.run()