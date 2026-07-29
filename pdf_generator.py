"""Module for generating detailed water distribution reports in PDF format."""

import os
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def gerar_relatorio_pdf(
    unidades: list[dict[str, Any]],
    val_fixo: float,
    t_fixa: float,
    val_var: float,
    total_moro: int,
    t_var: float,
    mes_ref: str,
) -> str:
    """Gera o relatório em PDF com o rateio detalhado das unidades."""
    os.makedirs("reports", exist_ok=True)
    nome_arquivo = f"relatorio_rateio_{mes_ref.replace('/', '_')}.pdf"
    caminho_pdf = os.path.join("reports", nome_arquivo)

    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    story: list[Any] = []
    styles = getSampleStyleSheet()

    # --- Estilos do Documento ---
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        alignment=1,  # Centralizado
        textColor=colors.HexColor("#1A2B4C"),
    )

    subtitle_style = ParagraphStyle(
        "SubTitleStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#555555"),
    )

    # --- Cabeçalho ---
    story.append(Paragraph("RELATÓRIO DE RATEIO DE ÁGUA & ESGOTO", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"Mês de Referência: <b>{mes_ref}</b>", subtitle_style))
    story.append(Spacer(1, 15))

    # --- Resumo Geral (Tabela de Custos) ---
    dados_resumo = [
        [
            "Custo Fixo Total",
            f"R$ {val_fixo:.2f}",
            "Taxa Fixa por Unid.",
            f"R$ {t_fixa:.2f}",
        ],
        [
            "Custo Variável Total",
            f"R$ {val_var:.2f}",
            "Taxa Var. por Morador",
            f"R$ {t_var:.2f}",
        ],
        [
            "Total de Moradores",
            str(total_moro),
            "Total Geral",
            f"R$ {(val_fixo + val_var):.2f}",
        ],
    ]

    tabela_resumo = Table(dados_resumo, colWidths=[130, 100, 150, 100])
    tabela_resumo.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F9")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#333333")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
            ]
        )
    )
    story.append(tabela_resumo)
    story.append(Spacer(1, 20))

    # --- Tabela Detalhada por Unidade ---
    dados_unidades = [
        ["Unid.", "Responsável", "Moradores", "Parc. Fixa", "Parc. Var.", "Total (R$)"]
    ]

    for u in sorted(unidades, key=lambda x: str(x.get("id", ""))):
        moro = int(u.get("moradores", 0))
        p_fixa = t_fixa
        p_var = t_var * moro
        v_total = p_fixa + p_var

        dados_unidades.append(
            [
                str(u.get("id", "")),
                str(u.get("nome_responsavel", "")),
                str(moro),
                f"R$ {p_fixa:.2f}",
                f"R$ {p_var:.2f}",
                f"R$ {v_total:.2f}",
            ]
        )

    tabela_detalhes = Table(dados_unidades, colWidths=[50, 180, 70, 80, 80, 80])
    tabela_detalhes.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A2B4C")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("ALIGN", (2, 0), (-1, -1), "CENTER"),
                ("ALIGN", (3, 0), (-1, -1), "RIGHT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#F9FAFB")],
                ),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            ]
        )
    )

    story.append(tabela_detalhes)

    # Constroi o arquivo PDF
    doc.build(story)
    return caminho_pdf
