from aima.logic import PropKB
from aima.utils import expr
import networkx
from fractions import gcd
from math import gcd

attributes = {
    'has_tawny_color', 'has_dark_spots', 'has_black_stripes',
    'has_long_neck', 'has_long_legs', 'has_hair', 'gives_milk',
    'has_feathers', 'flys', 'lays_eggs', 'eats_meat', 'has_pointed_teeth',
    'has_claws', 'has_forward_eyes', 'has_hooves', 'chews_cud',
    'does_not_fly', 'swims', 'is_black_and_white', 'appears_in_story_Ancient_Mariner',
    'flys_well'
}

classifications = {
    'cheetah', 'tiger', 'giraffe', 'zebra', 'ostrich',
    'penguin', 'albatross', 'mammal', 'bird', 'carnivore',
    'ungulate', 'unknown'
}

rules = [
    ({'mammal', 'carnivore', 'has_tawny_color', 'has_dark_spots'}, 'cheetah'),
    ({'mammal', 'carnivore', 'has_tawny_color', 'has_black_stripes'}, 'tiger'),
    ({'ungulate', 'has_long_neck', 'has_long_legs'}, 'giraffe'),
    ({'ungulate', 'has_black_stripes'}, 'zebra'),
    ({'bird', 'does_not_fly', 'has_long_neck'}, 'ostrich'),
    ({'bird', 'does_not_fly', 'swims', 'is_black_and_white'}, 'penguin'),
    ({'bird', 'appears_in_story_Ancient_Mariner', 'flys_well'}, 'albatross')
]

def infer_animal(attributes):
    inferred = set()
    while True:
        new_inferences = False
        for rule in rules:
            antecedent, consequent = rule
            if all(attr in attributes or attr in inferred for attr in antecedent) and consequent not in inferred:
                inferred.add(consequent)
                new_inferences = True
        if not new_inferences:
            break
    possible_animals = inferred.intersection(classifications)
    if possible_animals:
        return possible_animals.pop()
    else:
        return 'unknown'

def get_model(attributes):
    model = {}
    for attr in attributes:
        model[attr] = True
    return model

def kb_add_rules(kb, rules):
    for antecedent, consequent in rules:
        kb.tell(expr(f'({consequent} & {" & ".join(antecedent)})'))

def pl_resolution_infer(kb, attributes):
    model = get_model(attributes)
    alpha = expr('animal')
    kb.tell(expr('animal'))
    kb_add_rules(kb, rules)
    return pl_resolution(kb, alpha, model)

def infer_animal_aima(attributes):
    kb = PropKB()
    result = pl_resolution_infer(kb, attributes)
    if result:
        return result[0]['animal']
    else:
        return 'unknown'

def ask_user_for_attributes():
    user_attributes = set()
    print("Please answer with 'yes' or 'no' for the following attributes:")
    for attribute in attributes:
        response = input(f"Does the animal have {attribute.replace('_', ' ')}? ").strip().lower()
        if response == 'yes':
            user_attributes.add(attribute)
    return user_attributes

def main():
    user_input = ask_user_for_attributes()
    guessed_animal = infer_animal_aima(user_input)
    print("I guess that the animal is:", guessed_animal)

if __name__ == "__main__":
    main()