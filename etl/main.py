from process.entities.filmwork.etl import movies_etl
from state.state import JsonFileStorage, State


def start_etl():
    storage = JsonFileStorage()
    state = State(storage)

    movies_etl(state=state)


if __name__ == "__main__":
    start_etl()
