from flask import render_template, request, flash, session, redirect, url_for
from gigachat_gpt import gigachat_prompt


def setup_gigachat_routes(app):
    @app.route('/ask', methods=['GET', 'POST'])
    def ask_ai():
        if 'id' not in session:
            flash('Пожалуйста, войдите для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))

        answer = None
        if request.method == 'POST':
            prompt_text = request.form.get('prompt', '').strip()
            if not prompt_text:
                flash('Введите текст запроса', 'danger')
            else:
                try:
                    answer = gigachat_prompt(prompt_text)
                    app.logger.info(f"User {session['id']} made LLM request: {prompt_text}")
                except Exception as e:
                    flash(f'Ошибка при выполнении запроса: {str(e)}', 'danger')
                    app.logger.error(f"LLM error: {str(e)}")

        return render_template('ask_ai.html', answer=answer)
