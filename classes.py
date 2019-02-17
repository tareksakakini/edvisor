class frame:
    statement = ""
    question = ""
    answer = ""
    def __init__(self, statement, question, answer):
        self.statement = statement
        self.question = question
        self.answer = answer

class medication:
    name = frame("Your medication is called Metformin.", "What is your medication called?", "Metformin")
    purpose = frame("It is used to treat type 2 diabetes by helping to control the amount of glucose (sugar) in your blood.", "How does your medication treat your diabetes?", "By controlling the amount of sugar in my blood.")
    benefits = frame("If you take Metformin as directed, you will have a better blood sugar.  A better blood sugar helps to keep your heart, eyes, kidneys, and blood vessels healthy. ", "What are some benefits of taking your medication?", "Keep my heart, eyes, kidneys, and blood vessels healthy")
    dose = frame("Take one tablet of Metformin by mouth", "How many tablets should you take in one time?", "One tablet")
    frequency = frame("Take your medicine two times a day, with breakfast and with dinner. Swallow the table whole.", "How many times should you take the medicine in one day?", "Two times")
    missed_dose  = frame("If you forget to take your Metformin on time, take it as soon as you can. However, if it is almost time for the next dose, skip the missed dose and continue your regular schedule. Do not double dose to make up for a missed one.", "You forgot to take your medication and it is almost time for the next dose. How many tablets should you take?", "Only one tablet")
    duration = frame("Continue to take Metformin even if you feel well. Do not stop taking it without talking to your doctor.", "What should you do if you feel better after taking your medication for a while?", "I should ask my doctor if I can stop taking it")
    warnings = frame("Be sure to follow all exercise and diet recommendations from your doctor or dietitian. It is important to eat a healthy diet.", "Is it important to eat a healthy diet for your condition?", "Yes")
    mild_side_effects = frame("Some side effects are expected, but talk to your doctor if you notice diarrhea or metallic taste.", "What is an expected side effect?", "Diarrhea or metallic taste")
    dangerous_side_effects = frame("Other side effects can be serious. If you experience any of these symptoms, call your doctor immediately or get emergency treatment: itching or hives, swelling in face, hands, or mouth, stomach pain, or trouble breathing.", "What is a serious side effect?", "Itching or hives")

