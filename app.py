from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Contoh data toko bangunan
stores = [
    {"id": "1", "name": "Toko Bangunan Jaya", "description": "Menjual bahan bangunan lengkap."},
    {"id": "2", "name": "Bangun Sukses", "description": "Toko bahan bangunan murah dan berkualitas."},
]

# Detail setiap toko bangunan
store_details = {
    "1": {"id": "1", "name": "Toko Bangunan Jaya", "description": "Menjual bahan bangunan lengkap.", "customerReviews": []},
    "2": {"id": "2", "name": "Bangun Sukses", "description": "Toko bahan bangunan murah dan berkualitas.", "customerReviews": []},
}

class StoreList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(stores),
            "stores": stores
        }

class StoreDetail(Resource):
    def get(self, store_id):
        if store_id in store_details:
            return {
                "error": False,
                "message": "success",
                "store": store_details[store_id]
            }
        return {"error": True, "message": "Store not found"}, 404

class StoreSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [s for s in stores if query in s['name'].lower() or query in s['description'].lower()]
        return {
            "error": False,
            "founded": len(result),
            "stores": result
        }

class AddReview(Resource):
    def post(self):
        data = request.get_json()
        store_id = data.get('id')
        name = data.get('name')
        review = data.get('review')
        
        if store_id in store_details:
            new_review = {
                "name": name,
                "review": review,
                "date": datetime.now().strftime("%d %B %Y")
            }
            store_details[store_id]['customerReviews'].append(new_review)
            return {
                "error": False,
                "message": "success",
                "customerReviews": store_details[store_id]['customerReviews']
            }
        return {"error": True, "message": "Store not found"}, 404

class UpdateReview(Resource):
    def put(self):
        data = request.get_json()
        store_id = data.get('id')
        name = data.get('name')
        new_review_text = data.get('review')
        
        if store_id in store_details:
            reviews = store_details[store_id]['customerReviews']
            review_to_update = next((r for r in reviews if r['name'] == name), None)
            if review_to_update:
                review_to_update['review'] = new_review_text
                review_to_update['date'] = datetime.now().strftime("%d %B %Y")
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Store not found"}, 404

class DeleteReview(Resource):
    def delete(self):
        data = request.get_json()
        store_id = data.get('id')
        name = data.get('name')
        
        if store_id in store_details:
            reviews = store_details[store_id]['customerReviews']
            review_to_delete = next((r for r in reviews if r['name'] == name), None)
            if review_to_delete:
                reviews.remove(review_to_delete)
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Store not found"}, 404

api.add_resource(StoreList, '/stores')
api.add_resource(StoreDetail, '/stores/<string:store_id>')
api.add_resource(StoreSearch, '/stores/search')
api.add_resource(AddReview, '/stores/review')
api.add_resource(UpdateReview, '/stores/review/update')
api.add_resource(DeleteReview, '/stores/review/delete')

if __name__ == '__main__':
    app.run(debug=True)
