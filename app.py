from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'secret123'


questions = [
    {"text": "Как зовут главную героиню?", "options": ["a) Юки", "b) Кёко", "c) Саки"], "answer": "b"},
    
    {"text": "Какую фамилию носит главный герой?", "options": ["a) Мураками", "b) Исидзуми", "c) Миямура"], "answer": "c"},
    {"text": "Тебе хана щяс ток истенный фанат дальше справиться ты готов?", "options": ["b) НЕТ", "c) ДА"], "answer": "c"},

    {"text": "Какую причину Миямура называет, объясняя, почему он не заводил друзей до встречи с Хори?", 
     "options": ["a) Не было времени", "b) Не верил, что кому-то может быть интересен", "c) Он боялся отказа"], 
     "answer": "b"},

    {"text": "Какую неожиданную реакцию Хори проявляет, когда Миямура показывает агрессию?", 
     "options": ["a) Пугается и уходит", "b) Начинает плакать", "c) Её это привлекает"], 
     "answer": "c"},

    {"text": "Почему Ишикава вначале не может простить Миямуру?", 
     "options": ["a) Миямура раскрывает его секрет", "b) Думает, что Миямура украл у него шанс с Хори", "c) Он завидует оценкам Миямуры"], 
     "answer": "b"},

    {"text": "Что именно делает Торуу, чтобы помочь Йосифуми Танихой?", 
     "options": ["a) Делает домашку за него", "b) Встаёт за него перед буллерами", "c) Представляет его новым друзьям"], 
     "answer": "c"},

    {"text": "Какой эмоциональный конфликт возникает у Хори по поводу её сильного характера в отношениях?", 
     "options": ["a) Думает, что становится агрессивной", "b) Считает себя недостойной любви", "c) Боитcя, что отпугивает Миямуру"], 
     "answer": "c"},

    {"text": "Как зовут девушку, которая влюбляется в Миямуру после того, как он проявил себя вне школы?", 
     "options": ["a) Аюму", "b) Ёшиказу", "c) Хонока"], 
     "answer": "c"},

    {"text": "Почему Сенгоку постоянно нервничает, даже будучи президентом совета?", 
     "options": ["a) Из-за давления от родителей", "b) Потому что боится Саку", "c) Потому что боится ответственности"], 
     "answer": "b"},

    {"text": "Что означает фраза Миямуры: 'Я хотел бы исчезнуть, но чтобы никто этого не заметил'?", 
     "options": ["a) Он ищет внимания", "b) Он чувствует себя невидимым", "c) Он борется с депрессией и одиночеством"], 
     "answer": "c"},

    {"text": "Какая сцена лучше всего символизирует переход Миямуры от одиночества к принятию?", 
     "options": ["a) Когда он приглашён на день рождения", "b) Когда он сбривает волосы", "c) Когда он смеётся с друзьями в классе"], 
     "answer": "a"},

    {"text": "Какое значение имеет сцена с дождём, в которой Миямура стоит с зонтом рядом с Хори?", 
     "options": ["a) Он показывает, что заботится", "b) Это символ его желания разделить её бремя", "c) Это метафора очищения прошлого"], 
     "answer": "b"},

    {"text": "Какую черту характера Хори ненавидит в себе, но именно за неё Миямура её любит?", 
     "options": ["a) Вспыльчивость", "b) Упрямство", "c) Авторитарность"], 
     "answer": "a"},

    {"text": "Что делает Миямура в момент, когда Хори чувствует себя неуверенно в их отношениях?", 
     "options": ["a) Делает ей комплимент", "b) Говорит, что уйдёт", "c) Обещает, что будет с ней до конца"], 
     "answer": "c"},

    {"text": "Какова основная тема, раскрытая в отношениях Хори и Миямуры?", 
     "options": ["a) Сексуальное притяжение", "b) Принятие настоящей сущности друг друга", "c) Социальные различия"], 
     "answer": "b"},

    {"text": "Почему Миямура не хочет отпускать волосы обратно?", 
     "options": ["a) Боится снова выделяться", "b) Это часть его новой идентичности", "c) Потому что Хори просила"], 
     "answer": "b"},

    {"text": "Какой финальный жест символизирует зрелость их отношений?", 
     "options": ["a) Объятие", "b) Поцелуй", "c) Предложение пожениться"], 
     "answer": "c"}
]


@app.route('/')
def index():
    return redirect('/login')

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'qq11':
            session['username'] = username 
            flash('Login succ','success')
            return redirect('/quiz/1')
        else:
            flash('invalid ','danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("logged out",'info')
    return redirect('/login')


@app.route('/quiz/<int:qid>', methods=['GET', 'POST'])
def quiz(qid):
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        answer = request.form.get('answer')
        session[f'q{qid}'] = answer
        if qid < len(questions):
            return redirect(f'/quiz/{qid + 1}')
        else:
            return redirect('/result')
    question = questions[qid - 1]
    return render_template('quiz.html', qid=qid, question=question)


@app.route('/result')
def result():
    if 'username' not in session:
        return redirect('/login')
    score = 0
    user_answers = []
    for i, q in enumerate(questions, start=1):
        user_answer = session.get(f'q{i}')
        correct = q['answer']
        user_answers.append({'question': q['text'], 'your': user_answer, 'correct': correct})
        if user_answer == correct:
            score += 1
    flash('Quiz submitted!', 'success')
    return render_template('result.html', score=score, total=len(questions), username=session['username'], review=user_answers)

@app.route('/try-again')
def try_again():
    for i in range(1, len(questions) + 1):
        session.pop(f'q{i}', None)
    return redirect('/quiz/1')

if __name__ == '__main__':
    app.run(debug=True)
 