from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.student_controller import router as student_router

app = FastAPI(
    title="Sistema de Gestão Escolar API",
    description="API para gerenciamento de notas e frequência de alunos",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_router, prefix="/api", tags=["students"])

@app.get("/")
def read_root():
    return {
        "message": "Sistema de Gestão Escolar API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
