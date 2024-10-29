from pyknow import *


class DiabetesDetectionSystem(KnowledgeEngine):
    @DefFacts()
    def initial_fact(self):
        yield Fact()

    @Rule()
    def main(self):
        print("Welcome to the Diabetes Detection System.")
        print("Please answer the following questions to help with the diagnosis.")
        age = int(input("Enter your age: "))
        bmi = float(input("Enter your BMI: "))
        family_history = input("Do you have a family history of diabetes? (yes/no): ")
        increased_thirst = input("Have you been experiencing increased thirst? (yes/no): ")
        frequent_urination = input("Have you been experiencing frequent urination? (yes/no): ")
        
        self.declare(Fact(age=age, bmi=bmi, family_history=family_history.lower(), 
                          increased_thirst=increased_thirst.lower(), frequent_urination=frequent_urination.lower()))

    @Rule(AND(Fact(age=P(lambda x: x > 20)), Fact(bmi=P(lambda x: x > 0))))
    def rule_1(self):
        print("Rule 1: Age and BMI are within normal ranges.")

    @Rule(Fact(family_history="yes"))
    def rule_2(self):
        print("Rule 2: Family history of diabetes present.")

    @Rule(AND(Fact(increased_thirst="yes"), Fact(frequent_urination="yes")))
    def rule_3(self):
        print("Rule 3: Increased thirst and frequent urination reported.")

    @Rule(Fact(family_history="yes"), Fact(increased_thirst="yes"), Fact(frequent_urination="yes"))
    def diabetes_detected(self):
        print("Based on the information provided, you may have symptoms of diabetes. Please consult a doctor for further evaluation.")


if __name__ == "__main__":
    dds = DiabetesDetectionSystem()
    dds.reset()
    dds.run()
