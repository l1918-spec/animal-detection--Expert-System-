class Ask:
    def __init__(self, choices=['y', 'n']):
        self.choices = choices

    def ask(self):
        if len(self.choices[0]) > 1:
            for i, choice in enumerate(self.choices):
                print("{0}. {1}".format(i, choice), flush=True)
            while True:
                try:
                    choice_index = int(input("Enter your choice: "))
                    if choice_index in range(len(self.choices)):
                        return self.choices[choice_index]
                    else:
                        print("Invalid choice. Please enter a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            print("/".join(self.choices), flush=True)
            return input("Enter your choice: ")


class Content:
    def __init__(self, x):
        self.x = x


class If(Content):
    pass


class AND(Content):
    pass


class OR(Content):
    pass

rules = {
    'default': Ask(['y', 'n']),
    'color': Ask(['red-brown', 'black and white', 'other']),
    'pattern': Ask(['dark stripes', 'dark spots']),
    'mammal': If(OR(['hair', 'gives milk'])),
    'carnivor': If(OR([AND(['sharp teeth', 'claws', 'forward-looking eyes']), 'eats meat'])),
    'ungulate': If(AND([If('mammal'), OR(['has hooves', 'chews cud'])])),
    'bird': If(OR(['feathers', AND(['flies', 'lays eggs'])])),
    'animal:monkey': If([If('mammal'), If('carnivor'), 'color:red-brown', 'pattern:dark spots']),
    'animal:tiger': If([If('mammal'), If('carnivor'), 'color:red-brown', 'pattern:dark stripes']),
    'animal:giraffe': If([If('ungulate'), 'long neck', 'long legs', 'pattern:dark spots']),
    'animal:zebra': If([If('ungulate'), 'pattern:dark stripes']),
    'animal:ostrich': If([If('bird'), 'long neck', 'color:black and white', 'cannot fly']),
    'animal:penguin': If([If('bird'), 'swims', 'color:black and white', 'cannot fly']),
    'animal:albatross': If([If('bird'), 'flies well']),
    'animal:cat': If([If('mammal'), 'color:black and white', 'pattern:dark spots']),
    'animal:mouse': If([If('mammal'), 'color:other', 'pattern:dark spots']),
    'animal:cow': If([If('ungulate'), 'color:black and white']),
}

class KnowledgeBase:
    def __init__(self, rules):
        self.rules = rules
        self.memory = {}

    def get(self, name):
        if ':' in name:
            k, v = name.split(':')
            vv = self.get(k)
            return 'y' if v == vv else 'n'
        if name in self.memory:
            return self.memory[name]
        for field, expr in self.rules.items():
            if field == name or field.startswith(name + ":"):
                value = 'y' if field == name else field.split(':')[1]
                res = self.eval(expr, field=name)
                if res != 'y' and res != 'n' and value == 'y':
                    self.memory[name] = res
                    return res
                if res == 'y':
                    self.memory[name] = value  # Store the guessed animal name
                    return value
        res = self.eval(self.rules['default'], field=name)
        self.memory[name] = res
        return res


    def eval(self, expr, field=None):
        if isinstance(expr, Ask):
            print("Question for {}:".format(field))
            return expr.ask()
        elif isinstance(expr, If):
            return self.eval(expr.x)
        elif isinstance(expr, AND) or isinstance(expr, list):
            expr = expr.x if isinstance(expr, AND) else expr
            for x in expr:
                if self.eval(x) == 'n':
                    return 'n'
            return 'y'
        elif isinstance(expr, OR):
            for x in expr.x:
                if self.eval(x) == 'y':
                    return 'y'
            return 'n'
        elif isinstance(expr, str):
            return self.get(expr)
        else:
            print("Unknown expr: {}".format(expr))

kb = KnowledgeBase(rules)
animal_properties = kb.get('animal')
print("So I guess the animal is a  {}".format(kb.memory['animal']))
