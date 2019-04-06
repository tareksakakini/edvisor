class frame:
    statement = ""
    question = ""
    answer = []
    def __init__(self, statement, question, answer):
        self.statement = statement
        self.question = question
        self.answer = answer

class medication:
    #name = ""
    #purpose = ""
    #benefits = ""
    #dose = ""
    #frequency = ""
    #missed_dose = ""

    def __init__(self, json_object):
        [self.name, self.purpose, self.benefits, self.dose, self.frequency, self.missed_dose, self.duration, self.warnings, self.mild_side_effects, self.dangerous_side_effects] = [frame(json_object[key]["statement"], json_object[key]["question"], json_object[key]["answer"]) for key in ["name", "purpose", "benefits", "dose", "frequency", "missed_dose", "duration", "warnings", "mild_side_effects", "dangerous_side_effects"]]