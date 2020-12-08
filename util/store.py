from kivy.storage.jsonstore import JsonStore

store = JsonStore('storage/game_state.json')

def get(index, key):
    res = store.get(index)[key]
    print("RESULT: ", res)

def put():
    res = store.put("Eddy", id=1,first_name='Teddy', last_name='Klausner', module=0, scene=0, complete=False)
    print("RESULT: ", res)

def update_game_state(id, new_game_state):
    if id in store:
        store[id] = {
            'game_state': new_game_state,
            }
        return store[id]

    print("ID NOT FOUND")
    return

def update_assessment_state(user_id, module_id, question_id, correct):
    store[user_id]['game_state'][module_id]['assessment_state'] = {'question_id': question_id, 'correct': correct}

# new assessment question
def new_question():
    #
    #return
    pass


# create user in store if does not exist, return user
def init_user(user):
    id = user['id']
    if id not in store:
        store[id] = {
            'id': len(store),
            'game_state': [
                {
                    'module_id': 0,
                    'scene': 0,
                    'module_complete': False,
                    'assessment_state': [{'question_id' : 0, 'attempts' : 0, 'question_complete': False}],
                },
            ],
        }
    return store[id]
