from fastapi import Depends, FastAPI

app = FastAPI()


def limit_offset(limit: int = 100, offset: int = 0):
    return {'limit': limit, 'offset': offset}


@app.get('/squares')
def get_squares(
        paginator_params: dict = Depends(limit_offset)  # Подключите параметры limit и offset.
):
    """Возвращает квадраты чисел."""
    # Не меняйте следующую строчку.
    dataset = [x**2 for x in range(300)]

    dataset = dataset[paginator_params['offset']: paginator_params['offset'] + paginator_params['limit']]

    return dataset


@app.get('/unicode-symbols')
def get_unicode_symbols(
        paginator_params: dict = Depends(limit_offset)  # Подключите параметры limit и offset.
):
    """Возвращает символы юникода."""
    # Не меняйте следующие две строчки.
    dataset = [chr(x) for x in range(300)]
    dataset = ''.join(dataset)

    dataset = dataset[paginator_params['offset']: paginator_params['offset'] + paginator_params['limit']]

    return dataset
