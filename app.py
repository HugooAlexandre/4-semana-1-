from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# --- ESTRUTURAS DE DADOS ---

# Define os parâmetros que o formulário de configuração aceita.
# Estes dados informam a Inven!RA sobre os campos disponíveis.
PARAMS_DEFINITION = [
    { "name": "nivel_dificuldade", "type": "text/plain" },
    { "name": "tempo_maximo_minutos", "type": "integer" },
    { "name": "conteudos_em_curso", "type": "text/plain" },
    { "name": "classificacao_minima", "type": "integer" }
]

# Define a lista de métricas (analytics) que esta atividade é capaz de recolher.
# Separação entre qualitativas (URLs externos) e quantitativas (valores).
ANALYTICS_LIST_DEF = {
    "qualAnalytics": [
        { "name": "conteudo_mais_dificil", "type": "text/plain" },
        { "name": "erros_comuns", "type": "text/plain" }
    ],
    "quantAnalytics": [
        { "name": "conteudos_completos", "type": "integer" },
        { "name": "tempo_medio_resposta", "type": "integer" },
        { "name": "classificacao_final", "type": "integer" }
    ]
}

# --- ENDPOINTS DA API ---

# 1. URL DE CONFIGURAÇÃO (config_url)
# Retorna o código HTML do formulário que será exibido ao formador na Inven!RA.
# Não processa dados, apenas entrega a interface.
@app.route('/configuracao.html', methods=['GET'])
def get_config_ui():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Configuração da Atividade</title>
        <style>body { font-family: sans-serif; padding: 20px; }</style>
    </head>
    <body>
        <h2>Configurar Atividade</h2>
        <form id="configForm">
            <!-- Campos lidos automaticamente pela Inven!RA -->
            <label>Nível de Dificuldade:</label><br>
            <select name="nivel_dificuldade">
                <option value="basico">Básico</option>
                <option value="avancado">Avançado</option>
            </select><br><br>

            <label>Tempo Máximo (minutos):</label><br>
            <input type="number" name="tempo_maximo_minutos" value="30"><br><br>

            <label>Conteúdos Incluídos:</label><br>
            <input type="text" name="conteudos_em_curso" value="phishing,burlas"><br><br>
            
            <label>Classificação Mínima:</label><br>
            <input type="number" name="classificacao_minima" value="50">
        </form>
    </body>
    </html>
    """
    return make_response(html_content, 200)

# 2. DEFINIÇÃO DOS PARÂMETROS (json_params_url)
# Retorna um JSON descrevendo os tipos de dados do formulário de configuração.
@app.route('/json-params', methods=['GET'])
def get_json_params():
    return jsonify(PARAMS_DEFINITION)

# 3. DEPLOY DA ATIVIDADE (user_url)
# Chamado quando o formador disponibiliza a atividade.
# Recebe o ID da atividade via query string e retorna o URL de acesso para os alunos.
@app.route('/deploy-atividade', methods=['GET'])
def deploy_activity():
    # Extrai o ID da atividade da URL (ex: ?activityID=xyz)
    activity_id = request.args.get('activityID')
    
    if not activity_id:
        return jsonify({"error": "activityID obrigatorio"}), 400

    # Gera o URL onde o aluno deverá clicar para iniciar a atividade.
    # Em produção, este seria o domínio real da aplicação (ex: o domínio do Render).
    # Utilizamos request.host_url para garantir que o domínio se adapta ao ambiente.
    base_url = request.host_url.rstrip('/')
    student_access_url = f"{base_url}/atividade/iniciar?act={activity_id}"
    
    # Retorna o objeto JSON com o link de acesso.
    return jsonify({"access_url": student_access_url})

# 4. CONSULTA DE ANALYTICS (analytics_url)
# Recebe um pedido POST com o ID da atividade e retorna uma lista JSON
# contendo os dados detalhados de cada aluno associado a essa atividade.
@app.route('/analytics', methods=['POST'])
def get_analytics_data():
    # Tenta ler o JSON do corpo do pedido
    data = request.get_json(force=True, silent=True) or {}
    activity_id = data.get('activityID')

    base_url = request.host_url.rstrip('/')

    # Dados fictícios gerados para simular a resposta do servidor.
    # Estrutura: Lista de objetos, onde cada objeto representa um aluno.
    analytics_response = [
        {
            "inveniraStdID": "1001", # ID fictício do aluno 1
            "quantAnalytics": [
                { "name": "conteudos_completos", "value": 4 },
                { "name": "tempo_medio_resposta", "value": 120 },
                { "name": "classificacao_final", "value": 85 }
            ],
            "qualAnalytics": [
                # Links para visualizações detalhadas específicas deste aluno
                { "Student activity profile": f"{base_url}/qual/profile?std=1001&act={activity_id}" },
                { "Erros Comuns": f"{base_url}/qual/errors?std=1001&act={activity_id}" }
            ]
        },
        {
            "inveniraStdID": "1002", # ID fictício do aluno 2
            "quantAnalytics": [
                { "name": "conteudos_completos", "value": 2 },
                { "name": "tempo_medio_resposta", "value": 300 },
                { "name": "classificacao_final", "value": 40 }
            ],
            "qualAnalytics": [
                { "Student activity profile": f"{base_url}/qual/profile?std=1002&act={activity_id}" }
            ]
        }
    ]

    return jsonify(analytics_response)

# 5. LISTA DE ANALYTICS DISPONÍVEIS (analytics_list_url)
# Informa a Inven!RA sobre quais métricas este Activity Provider consegue medir.
@app.route('/lista-analytics', methods=['GET'])
def get_analytics_list():
    return jsonify(ANALYTICS_LIST_DEF)

# --- EXECUÇÃO ---
if __name__ == '__main__':
    # Configuração para execução local (desenvolvimento)
    app.run(host='0.0.0.0', port=5000, debug=True)