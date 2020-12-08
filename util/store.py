from kivy.storage.jsonstore import JsonStore

store = JsonStore('storage/game_state.json')

# internal: returns False if user_id or module_id is not in store; otherwise returns True
def _module_state_exists(user_id, module_id):
    if user_id not in store:
        print("ERROR: ID [{}] not found".format(user_id))
        return False
    if(module_id >= len(store[user_id]['game_state'])):
        print("ERROR: Module {} does not exist".format(module_id))
        return False
    return True

# returns the current state of the module
def current_module_state(user_id, module_id):
    if(_module_state_exists(user_id, module_id)):
        print(store[user_id]['game_state'][module_id])
        return store[user_id]['game_state'][module_id]

# updates the game state to reflect any module changes: module number, scene number, line number
def update_module_state(user_id, module_id, scene, line):
    if(_module_state_exists(user_id, module_id)):
        if(module_id == len(store[user_id]['game_state'])):
            store[user_id]['game_state'].append(_new_module(module_id))
        store[user_id]['game_state'][module_id] = {
            'module_id': module_id,
            'scene': scene,
            'line_number': line,
            'module_complete': False
        }
        store[user_id] = store[user_id]
        print(store[user_id])

# sets the module of specific user to complete
def complete_module_state(user_id, module_id):
    if(_module_state_exists(user_id, module_id)):
        store[user_id]['game_state'][module_id] = {
            'module_id': module_id,
            'module_complete': True
        }
        store[user_id] = store[user_id]
        print(store[user_id])

# creates an empty new module at id
def _new_module(id):
    module = {
        'module_id': id,
        'scene': 0,
        'line_number': 0,
        'module_complete': False,
        'assessment_state': [{'question_id' : 0, 'attempts' : 0, 'question_complete': False}],
    }
    return module

# creates user in store if does not exist, returns current state of user
def init_user(user):
    id = user['id']
    if id not in store:
        store[id] = {
            'id': len(store),
            'game_state': [_new_module(0)],
        }
        store[id] = store[id]
    return store[id]
