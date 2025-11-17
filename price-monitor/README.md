# Price Monitor

Uma ferramenta leve em Python para monitorar preços de produtos na web e enviar alertas por e-mail quando o preço atingir um valor alvo.

**Principais características**
- Raspagem (scraping) simples via `requests` + `BeautifulSoup`.
- Parsing inteligente de preços (suporte a formatos com separador de milhares e decimais).
- Histórico em CSV (`data/history.csv`).
- Notificações por e-mail via SMTP quando o preço fica abaixo do alvo.
- Fácil configuração via variáveis de ambiente (`.env`).

---

## Estrutura do projeto

- `src/` - código fonte
	- `main.py` - ponto de entrada que executa o scraping, atualiza histórico e notifica
	- `scraper.py` - funções de busca e parsing de preço (inclui tratamento específico para Amazon)
	- `notifier.py` - monta e envia e-mails HTML
	- `utils.py` - logger, helpers de parsing, manipulação do CSV de histórico
	- `config.py` - carrega variáveis de ambiente e monta a lista de produtos
- `data/` - saída de dados (ex.: `history.csv`)
- `logs/` - arquivos de log

---

## Requisitos

- Python 3.8+ (testado com 3.10/3.11)
- Pacotes Python (instale com pip):

```powershell
python -m pip install -r requirements.txt
```

Se não tiver `requirements.txt`, instale manualmente:

```powershell
python -m pip install requests beautifulsoup4 python-dotenv
```

---

## Configuração (variáveis de ambiente)

Crie um arquivo `.env` na raiz do projeto contendo as variáveis abaixo (exemplo):

```
EMAIL_USER=seuemail@gmail.com
EMAIL_PASS=sua_senha_app_ou_token
EMAIL_SMTP=smtp.gmail.com
EMAIL_PORT=587
PRODUCTS=Nome do Produto|https://url.do.produto|346.73
HISTORY_CSV=data/history.csv
LOG_FILE=logs/price_monitor.log
PRICE_SELECTOR=.a-price-whole
```

Notas:
- `PRODUCTS` aceita múltiplos itens separados por vírgula seguindo o formato `Nome|URL|PreçoAlvo`.
- `PRICE_SELECTOR` define o CSS selector usado pelo scraper. Para páginas Amazon use `.a-price-whole` (o projeto lida com fração separada `.a-price-fraction`).

---

## Uso

Executar o monitor manualmente:

```powershell
python src\main.py
```

Agendar execução:
- Windows Task Scheduler: agende `python <caminho>/src/main.py` conforme frequência desejada.
- Linux/macOS: use `cron` para rodar o mesmo comando.

---

## Logs e Histórico

- Logs são gravados em `logs/price_monitor.log` (definido em `LOG_FILE`).
- Histórico de preços é mantido em CSV (`data/history.csv`) com colunas: `date_time, product_name, price, url`.

---

## Problemas comuns e solução

- Erro de codificação (Windows): se o console levantar `UnicodeEncodeError` ao tentar escrever caracteres (ex.: emojis), remova emojis do assunto do e-mail ou configure o console para UTF-8. O projeto evita emojis no assunto por padrão para compatibilidade Windows.
- Se o scraper não encontrar um seletor, confirme o valor de `PRICE_SELECTOR` no `.env` ou verifique a estrutura do HTML da página. O `scraper` faz log do seletor usado (`Usando PRICE_SELECTOR: ...`).
- Preços formatados com duplicação de separador (ex.: `346,,73`): o parsing trata separadores de milhares e decimais — se encontrar problemas, verifique os fragments HTML (às vezes um `<span>` separado contém a vírgula decimal). Informe um exemplo do HTML e eu ajudo a ajustar o parser.

---

## Desenvolvimento

- Clone o repositório e crie um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

- Execute localmente e faça alterações em `src/`.

---

## Contribuição

Contribuições são bem-vindas. Abra uma issue descrevendo o problema ou feature, ou envie um pull request com mudanças pequenas e documentadas.

---

