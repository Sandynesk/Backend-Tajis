from fastapi import HTTPException, status
from models.user import AlunoCreate, AlunoResponse, ProfessorCreate, ProfessorResponse, LoginRequest, TokenResponse
from repositories.aluno_repository import AlunoRepository
from repositories.professor_repository import ProfessorRepository
from providers.database_provider import DatabaseProvider
from core.security import get_password_hash, verify_password, create_access_token

class AuthService:
    def __init__(self, db: DatabaseProvider):
        self.aluno_repo = AlunoRepository(db)
        self.prof_repo = ProfessorRepository(db)

    def register_aluno(self, aluno_data: AlunoCreate) -> AlunoResponse:
        # Verificar se email já existe
        if self.aluno_repo.get_by_email(aluno_data.email):
            raise HTTPException(status_code=400, detail="Email já cadastrado")
            
        # Hashear a senha
        hashed_password = get_password_hash(aluno_data.senha)
        
        # Preparar dados para inserção
        aluno_dict = aluno_data.model_dump(exclude={"senha"})
        aluno_dict["senha_hash"] = hashed_password
        
        # Salvar no banco
        created_aluno = self.aluno_repo.create(aluno_dict)
        return AlunoResponse.model_validate(created_aluno)

    def register_professor(self, professor_data: ProfessorCreate) -> ProfessorResponse:
        if self.prof_repo.get_by_email(professor_data.email):
            raise HTTPException(status_code=400, detail="Email já cadastrado")
            
        hashed_password = get_password_hash(professor_data.senha)
        
        prof_dict = professor_data.model_dump(exclude={"senha"})
        prof_dict["senha_hash"] = hashed_password
        
        created_prof = self.prof_repo.create(prof_dict)
        return ProfessorResponse.model_validate(created_prof)

    def login(self, login_data: LoginRequest) -> TokenResponse:
        # Tentar achar como aluno primeiro
        user = self.aluno_repo.get_by_email(login_data.email)
        role = "aluno"
        
        # Se não achar, tentar como professor
        if not user:
            user = self.prof_repo.get_by_email(login_data.email)
            role = "professor"
            
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos")
            
        # Verificar a senha
        if not verify_password(login_data.senha, user["senha_hash"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos")
            
        # Gerar o token
        access_token = create_access_token(subject=user["id"], role=role)
        
        user_data = {
            "id": user["id"],
            "nome": user.get("nome"),
            "email": user.get("email"),
            "role": role
        }
        
        return TokenResponse(access_token=access_token, token_type="bearer", role=role, user=user_data)
