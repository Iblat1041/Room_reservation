from fastapi import FastAPI, HTTPException

app = FastAPI()

COMMAND_TO_BOIL = 'Вскипятить воду'


def boil_water():
    pass


@app.post('/samovar_xxi')
def samovar_processing(command: str) -> str:
    if command != COMMAND_TO_BOIL:
        raise HTTPException(
            status_code=418,
            detail=command
        )

    boil_water()
    return 'Вода вскипела!'
