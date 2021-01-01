from kivy.storage.jsonstore import JsonStore

store = JsonStore('storage/game_state.json')
admin_store = JsonStore('storage/admin_state.json')


# internal: returns False if user_id or module_id is not in store; otherwise returns True
def _module_state_exists(user_id, module_id):
    if user_id not in store:
        print("ERROR: ID [{}] not found".format(user_id))
        return False
    if(module_id >= len(store[user_id]['game_state'])):
        print("ERROR (index out of bounds): Module {} does not exist".format(module_id))
        return False
    return True

# internal: returns False if question_id is not in store; otherwise returns True
def _question_state_exists(user_id, module_id, question_id):
    if(not _module_state_exists(user_id, module_id)):
        return False
    if(question_id >= len(store[user_id]['game_state'][module_id]['assessment_progress'])):
        print("ERROR (index out of bounds): Question {} does not exist".format(question_id))
        return False
    return True

# returns the current state of the assessment
def current_assessment_progress(user_id, module_id):
    if(_module_state_exists(user_id, module_id)):
        try:
            current_assessment_progress = store[user_id]['game_state'][module_id]['assessment_progress']
            return current_assessment_progress
        except Exception as err:
            print("ERROR: No assessment_progress keyword", err)
            return []

# updates the game state to reflect any assessment changes: module number, question number, attempts
def update_assessment_progress(user_id, module_id, question_id, attempts):
    if(_question_state_exists(user_id, module_id, question_id)):
        question_copy = dict(store[user_id]['game_state'][module_id]['assessment_progress'][question_id])
        question_copy['attempts'] = attempts
        store[user_id]['game_state'][module_id]['assessment_progress'][question_id] = question_copy
        store[user_id] = store[user_id]
    elif(user_id in store and question_id == len(store[user_id]['game_state'][module_id]['assessment_progress'])):
        store[user_id]['game_state'][module_id]['assessment_progress'].append(_new_question(question_id))
        store[user_id] = store[user_id]

    print("update assessment progress: " + str(store[user_id]))

# sets the assessment of specific module to completed
def complete_assessment_state(user_id, module_id):
    if(_module_state_exists(user_id, module_id)):
        module_copy = dict(store[user_id]['game_state'][module_id])
        module_copy['scene_id'] = 0
        module_copy['line_id'] = 0
        store[user_id]['game_state'][module_id] = module_copy
        store[user_id] = store[user_id]
        print("complete assessment state: " + str(store[user_id]))

# sets the question of specific module to complete
def complete_question_state(user_id, module_id, question_id):
    if(_question_state_exists(user_id, module_id, question_id)):
        question_copy = dict(store[user_id]['game_state'][module_id]['assessment_progress'][question_id])
        question_copy['question_complete'] = True
        store[user_id]['game_state'][module_id]['assessment_progress'][question_id] = question_copy
        store[user_id] = store[user_id]
        print("complete question state: " + str(store[user_id]))

# returns the current state of the module
def current_module_state(user_id, module_id):
    if(_module_state_exists(user_id, module_id)):
        print("current module state: " + str(store[user_id]['game_state'][module_id]))
        return store[user_id]['game_state'][module_id]
    else:
        print("module state doesn't exit")
        return None

# returns the state of the store
def current_state():
    return store

# clears the game state store
def clear_game_state():
    store.clear()
    print("CLEARING GAME STATE")

# checks if admin exists in admin_store
def admin_state_exists():
    current_state = get_admin_state()
    return current_state['admin'] is not None

# get *ADMIN* state
def get_admin_state():
    try:
        return admin_store['auth']
    except:
        admin_store['auth'] = {"admin": None, "users": None}
        print("Initializing admin store")
        return admin_store['admin']

def update_admin_state(admin, users):
    admin_store['auth'] = {'admin': admin, 'users': users}

# updates the game state to reflect any module changes: module number, scene number, line number
def update_module_state(user_id, module_id, scene, line):
    if(_module_state_exists(user_id, module_id)):
        module_copy = dict(store[user_id]['game_state'][module_id])
        module_copy['module_id'] = module_id
        module_copy['scene_id'] = scene
        module_copy['line_id'] = line
        store[user_id]['game_state'][module_id] = module_copy
        store[user_id] = store[user_id]
        print("store: " + str(store[user_id]))
    elif(user_id in store and module_id == len(store[user_id]['game_state'])):
        store[user_id]['game_state'].append(_new_module(module_id))
        store[user_id] = store[user_id]
        print("elif store: " + str(store[user_id]))

# sets the module of specific user to complete
def complete_module_state(user_id, module_id):
    if(_module_state_exists(user_id, module_id)):
        module_copy = dict(store[user_id]['game_state'][module_id])
        module_copy['module_complete'] = True
        store[user_id]['game_state'][module_id] = module_copy
        store[user_id] = store[user_id]
        print("complete module state: " + str(store[user_id]))

def new_user(id, state):
    if state:
        print("Populating returning user: [id] = ",id, "\n")
        store[id] = {
            'id': len(store),
            'game_state': [dict(state)],
        }
    else:
        print("Initializing new user: [id] = ",id, "\n")
        _init_user(id)

# creates an empty new question at id
def _new_question(id):
    question = {'question_id' : id, 'attempts' : 0, 'question_complete': False}
    return question

# creates an empty new module at id
def _new_module(id):
    module = {
        'module_id': id,
        'scene_id': 0,
        'line_id': 0,
        'module_complete': False,
        'assessment_progress': [_new_question(0)],
    }
    return module

# creates user in store if does not exist, returns current state of user
def _init_user(id):
    if id not in store:
        store[id] = {
            'id': len(store),
            'game_state': [_new_module(0)],
        }
        store[id] = store[id]
    return store[id]
