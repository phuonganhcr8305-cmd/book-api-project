from django.contrib import admin
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt

DEALERS = [
    {"id": 1, "name": "Kansas Auto Mall", "state": "Kansas"},
    {"id": 2, "name": "Sunflower Cars", "state": "Kansas"},
    {"id": 3, "name": "Texas Motors", "state": "Texas"},
    {"id": 4, "name": "California Wheels", "state": "California"},
]

REVIEWS = {
    1: [
        {"user": "Alice", "review": "Fantastic service and very friendly staff."},
        {"user": "Bob", "review": "Quick process and helpful dealer."}
    ],
    2: [
        {"user": "Charlie", "review": "Good prices and clean showroom."}
    ],
    3: [
        {"user": "David", "review": "Average experience."}
    ],
    4: [
        {"user": "Emma", "review": "Very professional team."}
    ]
}

def home(request):
    state = request.GET.get("state")
    dealers = DEALERS

    if state:
        dealers = [d for d in DEALERS if d["state"].lower() == state.lower()]

    username = request.user.username if request.user.is_authenticated else "Guest"

    dealer_html = ""
    for dealer in dealers:
        dealer_html += f"""
        <div style="border:1px solid #ccc; padding:12px; margin:10px 0; border-radius:8px;">
            <h3>{escape(dealer['name'])}</h3>
            <p><strong>ID:</strong> {dealer['id']}</p>
            <p><strong>State:</strong> {escape(dealer['state'])}</p>
            <a href="/dealer/{dealer['id']}" style="display:inline-block; margin-top:8px;">Review Dealer</a>
        </div>
        """

    return HttpResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dealers Home</title>
    </head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h1>Dealers Home Page</h1>
        <p><strong>Logged in user:</strong> {escape(username)}</p>
        <p><strong>Filter state:</strong> {escape(state) if state else "All"}</p>

        <div style="margin: 20px 0;">
            <a href="/?state=Kansas">Show Kansas Dealers</a> |
            <a href="/">Show All Dealers</a> |
            <a href="/dealers?state=Kansas">JSON Kansas Endpoint</a>
        </div>

        {dealer_html if dealer_html else "<p>No dealers found.</p>"}
    </body>
    </html>
    """)

def dealers_api(request):
    state = request.GET.get("state")
    dealers = DEALERS

    if state:
        dealers = [d for d in DEALERS if d["state"].lower() == state.lower()]

    return JsonResponse({"dealers": dealers})

def dealer_detail(request, dealer_id):
    dealer = next((d for d in DEALERS if d["id"] == dealer_id), None)

    if not dealer:
        return HttpResponse("<h1>Dealer not found</h1>", status=404)

    reviews = REVIEWS.get(dealer_id, [])

    reviews_html = ""
    for review in reviews:
        reviews_html += f"""
        <div style="border:1px solid #ddd; padding:10px; margin:10px 0; border-radius:6px;">
            <p><strong>User:</strong> {escape(review['user'])}</p>
            <p><strong>Review:</strong> {escape(review['review'])}</p>
        </div>
        """

    return HttpResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dealer Details</title>
    </head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h1>Dealer Details</h1>
        <h2>{escape(dealer['name'])}</h2>
        <p><strong>ID:</strong> {dealer['id']}</p>
        <p><strong>State:</strong> {escape(dealer['state'])}</p>

        <h2>Reviews</h2>
        {reviews_html if reviews_html else "<p>No reviews available.</p>"}
    </body>
    </html>
    """)
@csrf_exempt
def post_review(request, dealer_id):
    dealer = next((d for d in DEALERS if d["id"] == dealer_id), None)

    if not dealer:
        return HttpResponse("<h1>Dealer not found</h1>", status=404)

    # nếu submit
    if request.method == "POST":
        name = request.POST.get("name")
        review_text = request.POST.get("review")

        if dealer_id not in REVIEWS:
            REVIEWS[dealer_id] = []

        REVIEWS[dealer_id].append({
            "user": name,
            "review": review_text
        })

        return HttpResponse(f"""
        <html>
        <body style="font-family: Arial; padding:20px;">
            <h1>Review Added Successfully</h1>

            <h2>{escape(dealer['name'])}</h2>

            <p><strong>User:</strong> {escape(name)}</p>
            <p><strong>Review:</strong> {escape(review_text)}</p>

            <a href="/dealer/{dealer_id}">Back to Dealer</a>
        </body>
        </html>
        """)

    # nếu chưa submit → show form
    return HttpResponse(f"""
    <html>
    <body style="font-family: Arial; padding:20px;">
        <h1>Post Review</h1>

        <h2>{escape(dealer['name'])}</h2>

        <form method="POST">
            <label>Name:</label><br>
            <input type="text" name="name"><br><br>

            <label>Review:</label><br>
            <textarea name="review"></textarea><br><br>

            <button type="submit">Submit Review</button>
        </form>
    </body>
    </html>
    """)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("dealers", dealers_api),
    path("dealer/<int:dealer_id>", dealer_detail),
    path("dealer/<int:dealer_id>/review", post_review),
]