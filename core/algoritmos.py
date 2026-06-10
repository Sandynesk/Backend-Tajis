from typing import List, Dict, Any

def balancear_grupos_zigzag(alunos: List[Dict[str, Any]], tamanho_grupo: int) -> List[Dict[str, Any]]:
    """
    Distribui os alunos em grupos usando o algoritmo Zig-Zag (Snake Draft)
    para garantir balanceamento baseado na pontuação total.
    
    Os alunos devem vir pré-ordenados por pontuação_total (decrescente).
    
    Exemplo: 4 grupos (G1, G2, G3, G4)
    Rodada 1: 1->G1, 2->G2, 3->G3, 4->G4
    Rodada 2: 5->G4, 6->G3, 7->G2, 8->G1
    """
    if not alunos or tamanho_grupo <= 0:
        return []

    num_alunos = len(alunos)
    
    # Calcular quantos grupos precisaremos
    import math
    num_grupos = math.ceil(num_alunos / tamanho_grupo)
    
    # Inicializa os grupos vazios
    grupos = [{"nome": f"Grupo {i+1}", "alunos": []} for i in range(num_grupos)]
    
    # Se só houver 1 grupo, não precisa balancear
    if num_grupos == 1:
        grupos[0]["alunos"] = [a["id"] for a in alunos]
        return grupos
        
    # Zig-zag (Snake draft)
    direcao = 1 # 1 para frente (G1..GN), -1 para trás (GN..G1)
    grupo_idx = 0
    
    for aluno in alunos:
        grupos[grupo_idx]["alunos"].append(aluno["id"])
        
        # Move o índice
        grupo_idx += direcao
        
        # Se atingiu o limite (passou do último ou do primeiro), inverte a direção
        # e avança a "rodada" na mesma ponta
        if grupo_idx >= num_grupos:
            direcao = -1
            grupo_idx = num_grupos - 1
        elif grupo_idx < 0:
            direcao = 1
            grupo_idx = 0
            
    return grupos
