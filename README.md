
# 💧 Gestão de Água & Esgoto - Rateio (Kivy)

Aplicação desktop em Python desenvolvida com **Kivy** para cálculo, gestão e rateio proporcional de contas de água e esgoto em condomínios/unidades, consumindo dados do **Neon PostgreSQL** e gerando relatórios detalhados em **PDF**.

---

## 🚀 Funcionalidades

- **Cálculo Proporcional Automático**: Rateio do custo fixo por unidade e do custo variável proporcionalmente ao número de moradores.
- **Integração com Neon PostgreSQL**: Busca dinâmica e assíncrona da lista de unidades e moradores diretamente do banco de dados na nuvem.
- **Interface Responsiva (Kivy)**: Layout otimizado com navegação fluida via teclado (`Tab` / `Enter`) e lista de resultados rolável.
- **Geração de Relatório PDF**: Criação automática de relatórios em formato PDF prontos para impressão ou envio.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.12+
- **Gerenciador de Pacotes**: `uv`
- **Framework UI**: [Kivy](https://kivy.org/)
- **Database / Backend**: [Neon PostgreSQL](https://neon.com/)
- **Geração de PDF**: ReportLab (ou módulo local `pdf_generator`)
- **Automação CI/CD**: GitHub Actions (`keep_alive.yml`)

---

## 📂 Estrutura do Projeto

```text
water-billkiv-rateio/
├── reports/                   # Diretório de saída dos PDFs gerados (ignorado no Git)
├── app.py                     # Aplicação principal Kivy e regras de UI
├── database.py                # Integração e consultas ao Neon PostgreSQL
├── pdf_generator.py           # Módulo de geração de relatórios PDF
├── pyproject.toml             # Dependências do projeto (uv)
├── uv.lock                    # Trava de versões de dependências
└── README.md                  # Documentação do repositório
```
⚙️ Configuração e Instalação
1. Pré-requisitos
Certifique-se de ter o Python e o gerador de ambientes/pacotes uv instalados.

2. Clonar o Repositório

```Powershell
git clone [https://github.com/seu-usuario/water-billkiv-rateio.git](https://github.com/seu-usuario/water-billkiv-rateio.git)
cd water-billkiv-rateio
```

3. Instalar Dependências
Utilizando o uv:

```Powershell
uv sync
```

4. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com a URL de conexão do seu banco Neon:

```Plaintext
DATABASE_URL=postgresql://usuario:senha@ep-seu-projeto.us-east-2.aws.neon.tech/neondb?sslmode=require
```

🖥️ Como Executar a Aplicação
Rode a aplicação através do ambiente virtual gerenciado pelo uv:

```Powershell
uv run app.py
```

Fluxo de Uso:
Informe o Mês/Ano de Referência (ex: 07/2026).

Digite o Custo Fixo Total (R$) e pressione Tab ou Enter.

Digite o Custo Variável Total (R$).

Pressione Enter ou clique em Processar Rateio.

Visualize o resultado na tela e clique em Baixar PDF para abrir o relatório gerado.

✒️ Licença e Autor
Desenvolvido por Charles Duarte.