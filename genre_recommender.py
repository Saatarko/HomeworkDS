import pandas as pd
import ipywidgets as widgets

from IPython.display import display

def preprocess_popularity(ratings_df: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает DataFrame с movieId и средним рейтингом для каждого фильма.
    """
    popularity_df = ratings_df.groupby("movieId").agg(ave_rating=("rating", "mean"),
                                                      rating_count=("rating", "count")).reset_index()
    return popularity_df



def recommend_top_movies_by_genres(*genres, movies_df, popularity_df, top_n=10, min_votes=10):
    """
    Рекомендует топ-N фильмов по заданным жанрам, используя взвешенный рейтинг.

    Аргументы:
        *genres: Жанры (один или несколько), как строки.
        movies_df: датафрейм с фильмами и колонками movieId, title, genres.
        popularity_df: датафрейм с ave_rating и rating_count по movieId.
        top_n: сколько фильмов возвращать.
        min_votes: параметр "надежности" рейтинга (m в формуле).
    """
    # Объединение таблиц
    merged = pd.merge(movies_df, popularity_df, on="movieId")

    # Средний рейтинг по всей базе
    C = merged["ave_rating"].mean()

    # Фильтрация по жанрам (в порядке убывания количества совпадений)
    genres = [g.lower() for g in genres]
    merged["genre_match"] = merged["genres"].str.lower().apply(
        lambda g: sum(genre in g for genre in genres)
    )

    merged = merged[merged["genre_match"] > 0]

    if merged.empty:
        print("⚠️ Не найдено фильмов с точным совпадением жанров. Показываем ближайшие совпадения.")
        merged = pd.merge(movies_df, popularity_df, on="movieId")
        merged["genre_match"] = merged["genres"].str.lower().apply(
            lambda g: sum(genre in g for genre in genres)
        )
        merged = merged.sort_values(by="genre_match", ascending=False).head(top_n)

    # Вычисляем взвешенный рейтинг
    merged["weighted_rating"] = (
        (merged["rating_count"] / (merged["rating_count"] + min_votes)) * merged["ave_rating"] +
        (min_votes / (merged["rating_count"] + min_votes)) * C
    )

    # Финальный топ
    top_movies = merged.sort_values(by="weighted_rating", ascending=False).head(top_n)

    return top_movies[["title", "genres", "ave_rating", "rating_count", "weighted_rating"]]


def get_all_genres(movies_df: pd.DataFrame) -> list:
    """
    Возвращает уникальные жанры из всех фильмов.
    """
    genre_set = set()
    for genre_string in movies_df["genres"]:
        for g in genre_string.split("|"):
            genre_set.add(g.strip())
    return sorted(genre_set)


def show_recommendations(movies_df: pd.DataFrame, ratings_df: pd.DataFrame):
    """
    Интерактивный выбор жанров в Jupyter и вывод рекомендаций.
    """
    from IPython.display import display
    import ipywidgets as widgets
    from ipywidgets import Layout, Button, VBox

    # Получаем список всех жанров
    all_genres = get_all_genres(movies_df)

    # Создаем виджет для выбора жанров
    genre_select = widgets.SelectMultiple(
        options=all_genres,
        value=["Action"],
        description="Жанры",
        disabled=False
    )

    # Кнопка для получения рекомендаций
    button = Button(
        description="Показать рекомендации по жанру",
        layout=Layout(width='auto')  # автоматически подстраивается под текст
    )

    # Область для вывода рекомендаций
    output = widgets.Output()

    # Функция обработки клика по кнопке
    def on_click(b):
        output.clear_output()
        with output:
            # Предобработка данных о популярности
            popularity_df = preprocess_popularity(ratings_df)
            # Получаем выбранные жанры
            selected_genres = list(genre_select.value)
            # Получаем рекомендации
            recs = recommend_top_movies_by_genres(*selected_genres, movies_df=movies_df, popularity_df=popularity_df)
            # Отображаем результаты
            display(recs)

    # Привязываем обработчик события клика к кнопке
    button.on_click(on_click)

    # Формируем интерфейс
    ui = VBox([genre_select, button, output])

    # Отображаем интерфейс
    display(ui)