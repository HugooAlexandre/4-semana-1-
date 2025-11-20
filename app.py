from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# --- ESTRUTURAS DE DADOS ---

# 1. Definição dos parâmetros (Lido pela Inven!RA em /json-params)
PARAMS_DEFINITION = [
    { "name": "nivel_dificuldade", "type": "text/plain" },
    { "name": "tempo_maximo_minutos", "type": "integer" },
    { "name": "conteudos_em_curso", "type": "text/plain" },
    { "name": "classificacao_minima", "type": "integer" }
]

# 2. Definição das métricas disponíveis (Lido pela Inven!RA em /lista-analytics)
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

# --- ENDPOINTS (ROTAS) ---

# ROTA EXTRA: Página Inicial (para não dar erro 404 no link base)
@app.route('/')
def home():
    return "<h1>O Activity Provider está a funcionar!</h1><p>Use os endpoints específicos (/configuracao.html, etc.) para testar.</p>"

# 1. PÁGINA DE CONFIGURAÇÃO (config_url)
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

# 2. LISTA DE PARÂMETROS (json_params_url)
@app.route('/json-params', methods=['GET'])
def get_json_params():
    return jsonify(PARAMS_DEFINITION)

# 3. DEPLOY DA ATIVIDADE (user_url)
# Método GET conforme instruções atualizadas
@app.route('/deploy-atividade', methods=['GET'])
def deploy_activity():
    activity_id = request.args.get('activityID')
    
    if not activity_id:
        return jsonify({"error": "activityID em falta na URL"}), 400

    # Gera URL dinâmico baseando-se no domínio onde o servidor está a correr
    base_url = request.host_url.rstrip('/')
    student_access_url = f"{base_url}/atividade/iniciar?act={activity_id}"
    
    return jsonify({"access_url": student_access_url})

# 4. ANALYTICS DE UTILIZADOR (analytics_url)
# Retorna lista de alunos detalhada
@app.route('/analytics', methods=['POST'])
def get_analytics_data():
    data = request.get_json(force=True, silent=True) or {}
    activity_id = data.get('activityID')
    
    # Url base para links qualitativos
    base_url = request.host_url.rstrip('/')

    # Dados de exemplo (Mock) com a estrutura correta (Lista de Alunos)
    analytics_response = [
        {
            "inveniraStdID": "1001",
            "quantAnalytics": [
                { "name": "conteudos_completos", "value": 4 },
                { "name": "tempo_medio_resposta", "value": 120 },
                { "name": "classificacao_final", "value": 85 }
            ],
            "qualAnalytics": [
                { "Student activity profile": f"{base_url}/qual/profile?std=1001" },
                { "Erros Comuns": f"{base_url}/qual/errors?std=1001" }
            ]
        },
        {
            "inveniraStdID": "1002",
            "quantAnalytics": [
                { "name": "conteudos_completos", "value": 2 },
                { "name": "tempo_medio_resposta", "value": 300 },
                { "name": "classificacao_final", "value": 40 }
            ],
            "qualAnalytics": [
                { "Student activity profile": f"{base_url}/qual/profile?std=1002" }
            ]
        }
    ]

    return jsonify(analytics_response)

# 5. LISTA DE ANALYTICS DISPONÍVEIS (analytics_list_url)
@app.route('/lista-analytics', methods=['GET'])
def get_analytics_list():
    return jsonify(ANALYTICS_LIST_DEF)

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
