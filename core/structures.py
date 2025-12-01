import datetime

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class HistoryLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def add(self, command_name, custom_time=None):
        timestamp = custom_time if custom_time else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_node = Node({"cmd": command_name, "time": timestamp})
        
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.count += 1

    def get_all(self):
        elements = []
        current_node = self.head
        while current_node:
            elements.append(current_node.data)
            current_node = current_node.next
        return elements
    
    def get_penultimate(self):
        if self.count < 2:
            return None
        current_node = self.head
        while current_node.next and current_node.next.next:
            current_node = current_node.next
        return current_node.data

    def clear(self):
        self.head = None
        self.tail = None
        self.count = 0

class TreeNode:
    def __init__(self, text, is_leaf=False):
        self.text = text
        self.children = {}
        self.is_leaf = is_leaf

    def add_child(self, answer, node):
        self.children[answer.lower()] = node

class DialogueTree:
    def __init__(self, scenario_data=None):
        self.user_states = {}
        
        if scenario_data:
            self.root = self._build_tree_recursive(scenario_data)
        else:
            self.root = TreeNode("Aucun scénario chargé.", is_leaf=True)

    def _build_tree_recursive(self, data):
        if isinstance(data, str):
            return TreeNode(f"Conclusion : {data}", is_leaf=True)
        
        question_text = data.get("question", "Question inconnue ?")
        node = TreeNode(question_text, is_leaf=False)
        
        responses = data.get("reponses", {})
        for user_choice, next_step_data in responses.items():
            child_node = self._build_tree_recursive(next_step_data)
            node.add_child(user_choice, child_node)
            
        return node

    def get_node(self, user_id):
        if user_id not in self.user_states:
            self.user_states[user_id] = self.root
        return self.user_states[user_id]

    def set_next_node(self, user_id, choice):
        current_node = self.get_node(user_id)
        choice = choice.lower().strip()
        
        if choice in current_node.children:
            self.user_states[user_id] = current_node.children[choice]
            return self.user_states[user_id]
        return None

    def reset(self, user_id):
        self.user_states[user_id] = self.root

    def search_topic(self, node, topic):
        if topic.lower() in node.text.lower():
            return True
        for answer, child_node in node.children.items():
            if topic.lower() in answer:
                return True
            if self.search_topic(child_node, topic):
                return True
        return False