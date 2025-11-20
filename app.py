from flask import Flask, jsonify, request, make_response

app = Flask(__name__)


@app.route('/')
def home():
    return """
    <div style="text-align: center; padding-top: 50px; font-family: sans-serif;">
        <h1>Activity Provider Literacia Financeira</h1>
        <h3>Margarida Oliveira</h3>
        <p>O servidor está online e pronto para receber pedidos da Inven!RA.</p>
    </div>
    """



# Define os parâmetros de configuração aceites pela atividade.
PARAMS_DEFINITION = [
    { "name": "modulos_ativos", "type": "text/plain" },
    { "name": "nivel_dificuldade", "type": "text/plain" },
    { "name": "nota_minima_aprovacao", "type": "integer" },
    { "name": "limite_tempo_minutos", "type": "integer" }
]

# Define a lista de métricas (analytics).
ANALYTICS_LIST_DEF = {
    "qualAnalytics": [
        { "name": "feedback_modulos", "type": "text/plain" },
        { "name": "erros_comuns", "type": "text/plain" }
    ],
    "quantAnalytics": [
        { "name": "modulos_concluidos", "type": "integer" },
        { "name": "tempo_total_minutos", "type": "integer" },
        { "name": "pontuacao_orcamento", "type": "integer" },
        { "name": "pontuacao_poupanca", "type": "integer" },
        { "name": "pontuacao_juros", "type": "integer" },
        { "name": "pontuacao_consumo", "type": "integer" }
    ]
}



# 1. URL DE CONFIGURAÇÃO
@app.route('/edu-financeira/config.html', methods=['GET'])
def get_config_ui():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Configuração da Atividade</title>
        <style>body { font-family: sans-serif; padding: 20px; } label { font-weight: bold; }</style>
    </head>
    <body>
        <h2>Configurar Atividade: Educação Financeira</h2>
        <form id="configForm">
            <label>Módulos a incluir (separados por vírgula):</label><br>
            <input type="text" name="modulos_ativos" value="orcamento,poupanca,juros,consumo" style="width: 300px;"><br><br>

            <label>Nível de Dificuldade:</label><br>
            <select name="nivel_dificuldade">
                <option value="basico">Básico</option>
                <option value="intermedio" selected>Intermédio</option>
                <option value="avancado">Avançado</option>
            </select><br><br>

            <label>Nota Mínima de Aprovação (%):</label><br>
            <input type="number" name="nota_minima_aprovacao" value="50"><br><br>
            
            <label>Limite de Tempo (minutos):</label><br>
            <input type="number" name="limite_tempo_minutos" value="45">
        </form>
    </body>
    </html>
    """
    return make_response(html_content, 200)

# 2. URL DE PARÂMETROS JSON
@app.route('/edu-financeira/params', methods=['GET'])
def get_json_params():
    return jsonify(PARAMS_DEFINITION)

# 3. URL DE DEPLOY
@app.route('/edu-financeira/deploy', methods=['GET'])
def deploy_activity():
    activity_id = request.args.get('activityID')
    
    if not activity_id:
        return jsonify({"error": "activityID obrigatorio"}), 400

    base_url = request.host_url.rstrip('/')
    student_access_url = f"{base_url}/atividade/run?act={activity_id}"
    
    return jsonify({"access_url": student_access_url})

# 4. URL DE ANALYTICS
@app.route('/edu-financeira/analytics', methods=['POST'])
def get_analytics_data():
    data = request.get_json(force=True, silent=True) or {}
    activity_id = data.get('activityID', 'unknown')

    base_url = request.host_url.rstrip('/')

    analytics_response = [
        {
            "inveniraStdID": "1001",
            "quantAnalytics": [
                { "name": "modulos_concluidos", "value": 4 },
                { "name": "tempo_total_minutos", "value": 35 },
                { "name": "pontuacao_orcamento", "value": 90 },
                { "name": "pontuacao_poupanca", "value": 85 },
                { "name": "pontuacao_juros", "value": 70 },
                { "name": "pontuacao_consumo", "value": 95 }
            ],
            "qualAnalytics": [
                { "Relatorio Detalhado": f"{base_url}/report/detail?std=1001&act={activity_id}" },
                { "Erros Comuns": f"{base_url}/report/errors?std=1001&act={activity_id}" }
            ]
        },
        {
            "inveniraStdID": "1002",
            "quantAnalytics": [
                { "name": "modulos_concluidos", "value": 2 },
                { "name": "tempo_total_minutos", "value": 45 },
                { "name": "pontuacao_orcamento", "value": 60 },
                { "name": "pontuacao_poupanca", "value": 50 },
                { "name": "pontuacao_juros", "value": 20 },
                { "name": "pontuacao_consumo", "value": 0 }
            ],
            "qualAnalytics": [
                { "Relatorio Detalhado": f"{base_url}/report/detail?std=1002&act={activity_id}" }
            ]
        }
    ]

    return jsonify(analytics_response)

# 5. URL DE LISTA DE ANALYTICS
@app.route('/edu-financeira/analytics-list', methods=['GET'])
def get_analytics_list():
    return jsonify(ANALYTICS_LIST_DEF)

# Inicialização do servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
