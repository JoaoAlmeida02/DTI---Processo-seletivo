from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller.estudanteController import router as estudante_router

app = FastAPI(
    title="Sistema de Gestão Escolar API",
    description="API para gerenciamento de notas e frequência de alunos",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(estudante_router, prefix="/api", tags=["estudantes"])


@app.get("/")
def read_root():
    return {
        "message": "Sistema de Gestão Escolar API",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
