from core.algoritmos import balancear_grupos_zigzag

def test_zigzag_team_formation():
    alunos = [
        {"id": 1, "nome": "A", "pontuacao_total": 10},
        {"id": 2, "nome": "B", "pontuacao_total": 9},
        {"id": 3, "nome": "C", "pontuacao_total": 8},
        {"id": 4, "nome": "D", "pontuacao_total": 7},
        {"id": 5, "nome": "E", "pontuacao_total": 6},
        {"id": 6, "nome": "F", "pontuacao_total": 5},
    ]
    # Com 3 alunos por grupo, teremos 2 grupos
    grupos = balancear_grupos_zigzag(alunos, tamanho_grupo=3)
    
    assert len(grupos) == 2
    assert len(grupos[0]["alunos"]) == 3
    assert len(grupos[1]["alunos"]) == 3
    
    # Zig-Zag logic:
    # 1º A(1) vai pro G1, 2º B(2) vai pro G2.
    # Inverte: 3º C(3) vai pro G2, 4º D(4) vai pro G1.
    # Inverte: 5º E(5) vai pro G1, 6º F(6) vai pro G2.
    
    # Verifica G1
    assert grupos[0]["alunos"] == [1, 4, 5]
    
    # Verifica G2
    assert grupos[1]["alunos"] == [2, 3, 6]

def test_zigzag_empty():
    assert balancear_grupos_zigzag([], 3) == []
    
def test_zigzag_one_group():
    alunos = [{"id": 1}, {"id": 2}]
    grupos = balancear_grupos_zigzag(alunos, 5)
    assert len(grupos) == 1
    assert grupos[0]["alunos"] == [1, 2]
