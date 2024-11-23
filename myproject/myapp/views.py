from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to the Django app!"})

import matplotlib
matplotlib.use('Agg')  # Use the Agg backend to avoid Tkinter warnings

from io import BytesIO
import matplotlib.pyplot as plt
from pymongo import MongoClient
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from bson import ObjectId
from decouple import config



mongo_client_host = config('MONGO_CLIENT_HOST')
client = MongoClient(mongo_client_host)

# Access the database and collection
db = client["user"]
users_collection = db["user1"]

class UserProgressView(APIView):
    def get(self, request, user_id):
        try:
            # Validate user_id format
            if not ObjectId.is_valid(user_id):
                return JsonResponse({"error": "Invalid user_id format"}, status=400)

            # Fetch user data from MongoDB
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                return JsonResponse({"error": "User not found"}, status=404)

            # Extract relevant data
            completed_courses = len(user.get("completed_courses", []))
            current_courses = len(user.get("current_courses", []))
            wishlist_courses = len(user.get("wishlist", []))

            # Prepare data for plotting
            categories = ["Completed", "Current", "Wishlist"]
            values = [completed_courses, current_courses, wishlist_courses]

            # Updated color scheme
            colors = ['#ff9800', '#8bc34a', '#3f51b5']  # New color scheme: Orange, Green, Blue

            # Create a figure with two subplots (horizontal bar and donut chart)
            fig, axs = plt.subplots(1, 2, figsize=(14, 6))

            # Horizontal Bar Chart
            axs[0].barh(categories, values, color=colors)
            axs[0].set_title(f"User Progress: {user.get('fName', 'N/A')} {user.get('lName', 'N/A')}")
            axs[0].set_xlabel("Number of Courses")
            axs[0].set_ylabel("Category")
            axs[0].grid(axis='x', linestyle='--', alpha=0.7)

            # Donut Chart
            wedges, texts, autotexts = axs[1].pie(values, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops=dict(width=0.4))
            axs[1].set_title("User Progress (Donut)")

            # Adjust layout
            plt.tight_layout()

            # Save the plot to a BytesIO object
            buf = BytesIO()
            plt.savefig(buf, format="png")
            plt.close()  # Close the plot to free memory
            buf.seek(0)

            # Return the plot as an HTTP response
            return HttpResponse(buf.getvalue(), content_type="image/png")

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"error": "Error generating user progress", "details": str(e)}, status=500)
