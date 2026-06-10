def xp_bar(xp_atual: int, xp_proximo: int, nivel: int) -> str:
    percent = min(int((xp_atual / xp_proximo) * 100), 100)
    return f"""
    <div style="margin: 8px 0 16px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <span style="font-family:'Geist Mono',monospace; font-size:11px;
                         color:#52525B; letter-spacing:0.06em;">
                NÍVEL {nivel}
            </span>
            <span style="font-family:'Geist Mono',monospace; font-size:11px; color:#52525B;">
                {xp_atual} / {xp_proximo} XP
            </span>
        </div>
        <div style="background:#1A1A1A; border-radius:99px; height:6px; width:100%; overflow:hidden;">
            <div style="
                height:100%; border-radius:99px;
                background:linear-gradient(90deg, #7C3AED, #A78BFA);
                width:{percent}%;
                transition: width 1.2s cubic-bezier(0.16,1,0.3,1);
            "></div>
        </div>
    </div>
    """

def stat_card(label: str, valor: str, icone_svg: str = "", delta: str = "") -> str:
    delta_html = f'<span style="font-size:11px;color:#10B981;margin-top:4px;">{delta}</span>' if delta else ""
    return f"""
    <div style="
        background:#111111; border:1px solid rgba(255,255,255,0.06);
        border-radius:12px; padding:16px 20px;
        display:flex; flex-direction:column; gap:4px;
    ">
        <span style="font-family:'Geist Mono',monospace; font-size:11px;
                     text-transform:uppercase; letter-spacing:0.08em; color:#52525B;">
            {label}
        </span>
        <span style="font-family:'Inter Tight',sans-serif; font-weight:700;
                     font-size:28px; color:#F5F5F5; letter-spacing:-0.03em;">
            {valor}
        </span>
        {delta_html}
    </div>
    """

def badge(texto: str, tipo: str = "default") -> str:
    estilos = {
        "default":  ("rgba(124,58,237,0.15)", "#A78BFA"),
        "gold":     ("#78350F", "#F59E0B"),
        "success":  ("rgba(16,185,129,0.15)", "#10B981"),
        "danger":   ("rgba(239,68,68,0.15)", "#EF4444"),
        "muted":    ("rgba(255,255,255,0.05)", "#52525B"),
    }
    bg, cor = estilos.get(tipo, estilos["default"])
    return f"""
    <span style="
        background:{bg}; color:{cor};
        font-family:'Geist Mono',monospace; font-size:11px; font-weight:500;
        letter-spacing:0.04em; padding:3px 10px;
        border-radius:99px; white-space:nowrap;
    ">{texto}</span>
    """

def challenge_card(titulo: str, descricao: str, status: str, pontos: int) -> str:
    status_map = {
        "em_progresso": ("Em progresso", "default"),
        "concluido":    ("Concluído", "success"),
        "bloqueado":    ("Bloqueado", "muted"),
        "disponivel":   ("Disponível", "default"),
    }
    label, tipo = status_map.get(status, ("—", "muted"))
    borda = "rgba(124,58,237,0.4)" if status in ("em_progresso", "disponivel") else "rgba(255,255,255,0.06)"
    return f"""
    <div style="
        background:#111111; border:1px solid {borda};
        border-left: 2px solid {'#7C3AED' if status == 'em_progresso' else borda};
        border-radius:12px; padding:16px 20px; margin-bottom:10px;
        transition: background 150ms ease;
    ">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
            <span style="font-family:'Inter Tight',sans-serif; font-weight:500;
                         font-size:15px; color:#F5F5F5;">
                {titulo}
            </span>
            {badge(label, tipo)}
        </div>
        <p style="font-family:'Geist Sans',sans-serif; font-size:13px;
                  color:#A1A1AA; margin:0 0 12px; line-height:1.5;">
            {descricao}
        </p>
        <span style="font-family:'Geist Mono',monospace; font-size:11px; color:#52525B;">
            +{pontos} pts
        </span>
    </div>
    """

def divider(label: str = "") -> str:
    if label:
        return f"""
        <div style="display:flex; align-items:center; gap:12px; margin:20px 0;">
            <div style="flex:1; height:1px; background:rgba(255,255,255,0.05);"></div>
            <span style="font-family:'Geist Mono',monospace; font-size:11px;
                         color:#52525B; letter-spacing:0.08em; white-space:nowrap;">
                {label}
            </span>
            <div style="flex:1; height:1px; background:rgba(255,255,255,0.05);"></div>
        </div>
        """
    return '<div style="height:1px; background:rgba(255,255,255,0.05); margin:20px 0;"></div>'

def ranking_row(posicao: int, nome: str, pontos: int, nivel: int, is_current_user: bool = False) -> str:
    pos_cor = {"1": "#F59E0B", "2": "#A1A1AA", "3": "#CD7C3E"}.get(str(posicao), "#52525B")
    bg = "rgba(124,58,237,0.08)" if is_current_user else "transparent"
    borda = "rgba(124,58,237,0.3)" if is_current_user else "transparent"
    return f"""
    <div style="
        display:flex; align-items:center; gap:16px;
        padding:12px 16px; border-radius:10px;
        background:{bg}; border:1px solid {borda};
        margin-bottom:4px;
    ">
        <span style="font-family:'Inter Tight',sans-serif; font-weight:700;
                     font-size:16px; color:{pos_cor}; min-width:28px;">
            #{posicao}
        </span>
        <span style="font-family:'Geist Sans',sans-serif; font-size:14px;
                     color:#F5F5F5; flex:1;">
            {nome}
        </span>
        <span style="font-family:'Geist Mono',monospace; font-size:11px; color:#52525B;">
            Nv {nivel}
        </span>
        <span style="font-family:'Inter Tight',sans-serif; font-weight:500;
                     font-size:14px; color:#A78BFA;">
            {pontos:,} pts
        </span>
    </div>
    """
