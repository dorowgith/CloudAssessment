# Flask app will be initialized here
from flask import Flask, render_template, request, redirect, url_for, session
import os # For a more robust secret key generation if needed

SCORING_MULTIPLIERS = {
    "total": 1.0,
    "parcial": 0.5,
    "nao_atendida": 0.0
}

ASSESSMENT_DATA = [
    {
        "id": "arquitetura",
        "name": "Arquitetura",
        "questions": [
            {"id": "arq1", "text": "A arquitetura da solução está bem definida e documentada?", "weight": 5},
            {"id": "arq2", "text": "A solução utiliza componentes e serviços adequados para os requisitos?", "weight": 4},
            {"id": "arq3", "text": "A escalabilidade da arquitetura foi considerada?", "weight": 4},
        ]
    },
    {
        "id": "resiliencia",
        "name": "Resiliência",
        "questions": [
            {"id": "res1", "text": "Existem mecanismos de backup e restauração de dados definidos e testados?", "weight": 5},
            {"id": "res2", "text": "A solução possui alta disponibilidade e tolerância a falhas?", "weight": 5},
            {"id": "res3", "text": "Existe um plano de recuperação de desastres (DRP)?", "weight": 3},
        ]
    },
    {
        "id": "cyber_seguranca",
        "name": "Cyber Segurança",
        "questions": [
            {"id": "sec1", "text": "As melhores práticas de segurança foram aplicadas no desenvolvimento e configuração?", "weight": 5},
            {"id": "sec2", "text": "Existem controles de acesso e autenticação robustos?", "weight": 4},
            {"id": "sec3", "text": "A solução é monitorada quanto a atividades suspeitas e vulnerabilidades?", "weight": 4},
        ]
    },
    {
        "id": "governanca",
        "name": "Governança",
        "questions": [
            {"id": "gov1", "text": "Os papéis e responsabilidades relacionados à operação da solução estão claros?", "weight": 4},
            {"id": "gov2", "text": "Existem processos para gestão de mudanças e configuração?", "weight": 4},
            {"id": "gov3", "text": "A conformidade com políticas e regulações é auditada?", "weight": 3},
        ]
    },
    {
        "id": "finops",
        "name": "FinOps",
        "questions": [
            {"id": "fin1", "text": "Existe um acompanhamento e otimização contínua dos custos da solução em nuvem?", "weight": 5},
            {"id": "fin2", "text": "As instâncias e serviços estão dimensionados corretamente para evitar desperdícios?", "weight": 4},
            {"id": "fin3", "text": "Há visibilidade sobre os gastos e alocação de custos por centro de custo ou projeto?", "weight": 3},
        ]
    }
]

app = Flask(__name__)
# IMPORTANT: Add a secret key for session management
app.secret_key = os.urandom(24) # Or a fixed string for development: 'your_very_secret_key'

@app.route('/')
def assessment_form():
    return render_template('form.html', categories=ASSESSMENT_DATA, answer_options=list(SCORING_MULTIPLIERS.keys()))

@app.route('/submit', methods=['POST'])
def submit_assessment():
    category_scores = {}
    # detailed_question_scores = {} # Optional: for more granular tracking

    for category in ASSESSMENT_DATA:
        current_category_score = 0
        # if category['id'] not in detailed_question_scores:
        #     detailed_question_scores[category['id']] = {}

        for question in category['questions']:
            question_id = question['id']
            selected_option_key = request.form.get(question_id)

            if selected_option_key: # Ensure the question was answered
                weight = question['weight']
                multiplier = SCORING_MULTIPLIERS[selected_option_key]
                question_score = weight * multiplier
                current_category_score += question_score
                # detailed_question_scores[category['id']][question_id] = question_score
            # else:
                # Handle unanswered questions if necessary, though 'required' on radio should prevent this
                # detailed_question_scores[category['id']][question_id] = 0


        category_scores[category['id']] = {
            'name': category['name'], # Store name for easy access in template
            'score': current_category_score
        }


    session['category_scores'] = category_scores
    # session['detailed_scores'] = detailed_question_scores # Optional

    return redirect(url_for('show_results')) # Assuming results route is named 'show_results'

@app.route('/results')
def show_results():
    category_scores = session.get('category_scores', {})
    # Prepare data for Chart.js: labels and actual score data
    labels = [details['name'] for details in category_scores.values()]
    scores = [details['score'] for details in category_scores.values()]
    
    # Max possible score per category (for radar chart scaling, if needed, or just use actual scores)
    # This is a bit more complex as weights vary. For now, Chart.js will auto-scale.
    # A more advanced version might calculate max possible score for each category.

    return render_template('results.html', 
                           labels=labels, 
                           scores=scores, 
                           category_data=category_scores) # Pass full data if needed for display

if __name__ == '__main__':
    app.run(debug=True)
