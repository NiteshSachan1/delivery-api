from flask import Flask, request, jsonify 
import itertools

app = Flask(__name__)

products = {
    'A': ('C1', 3), 'B': ('C1', 2), 'C': ('C1', 8),
    'D': ('C2', 12), 'E': ('C2', 25), 'F': ('C2', 15),
    'G': ('C3', 0.5), 'H': ('C3', 1), 'I': ('C3', 2),
}

distances = {
    ('C1', 'L1'): 3,    ('C2', 'L1'): 2.5,  ('C3', 'L1'): 2,
    ('C1', 'C2'): 4,    ('C2', 'C1'): 4,
    ('C2', 'C3'): 3,    ('C3', 'C2'): 3,
    ('C1', 'C3'): 5,    ('C3', 'C1'): 5
}

def compute_cost(path, center_weights):
    total_cost = 0
    current_weight = 0
    visited = set()

    for i in range(len(path) - 1):
        src, dst = path[i], path[i+1]

        if dst in center_weights and dst not in visited:
            current_weight += center_weights[dst]
            visited.add(dst)

        cost_per_unit = 10 if current_weight <= 5 else 8
        total_cost += distances[(src, dst)] * cost_per_unit

    return total_cost

@app.route('/')
def home():
    return 'Delivery Cost Calculator API'

@app.route('/calculate_cost', methods=['POST'])
def calculate_cost():
    try:
        order = request.get_json()
        center_weights = {}
        for product, qty in order.items():
            if product in products and qty > 0:
                center, weight = products[product]
                center_weights[center] = center_weights.get(center, 0) + weight * qty

        if not center_weights:
            return jsonify({'error': 'No valid products in the order'}), 400

        centers = list(center_weights.keys())
        min_cost = float('inf')

        for perm in itertools.permutations(centers):
            path = list(perm) + ['L1']
            cost = compute_cost(path, center_weights)
            if cost < min_cost:
                min_cost = cost

        return jsonify({'minimum_cost': int(min_cost)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
