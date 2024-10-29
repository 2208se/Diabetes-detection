from flask import Flask, render_template, request
from experta import *

app = Flask(__name__)

class DiabetesDetectionSystem(KnowledgeEngine):
    @DefFacts()
    def initial_fact(self):
        yield Fact()

    @Rule()
    def main(self):
        pass

    @Rule(AND(Fact(age=P(lambda x: int(x) > 20)), Fact(bmi=P(lambda x: float(x) > 0))))
    def rule_1(self):
        pass

    @Rule(Fact(family_history="yes"))
    def rule_2(self):
        self.declare(Fact(family_history="present"))

    @Rule(AND(Fact(increased_thirst="yes"), Fact(frequent_urination="yes")))
    def rule_3(self):
        self.declare(Fact(symptoms="present"))

    @Rule(Fact(family_history="yes"), Fact(increased_thirst="yes"), Fact(frequent_urination="yes"))
    def diabetes_detected(self):
        self.declare(Fact(diabetes_detected=True))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dds = DiabetesDetectionSystem()
        dds.reset()

        age = request.form['age']
        bmi = request.form['bmi']
        family_history = request.form['family_history']
        increased_thirst = request.form['increased_thirst']
        frequent_urination = request.form['frequent_urination']

        dds.declare(Fact(age=int(age), bmi=float(bmi), family_history=family_history.lower(),
                         increased_thirst=increased_thirst.lower(), frequent_urination=frequent_urination.lower()))
        dds.run()

        # Check if any facts contain the 'diabetes_detected' attribute
        if any(isinstance(fact, Fact) and fact.get('diabetes_detected') for fact in dds.facts):
            result = "Based on the information provided, you may have symptoms of diabetes. Please consult a doctor for further evaluation."
        else:
            result = "No symptoms of diabetes detected."

        return render_template('result.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
