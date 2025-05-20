from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import os
import requests

google_maps_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

class PlaceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Query parameter is required"}, status=400)
        url = f"{google_maps_url}?query={query}&key={google_maps_api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            return Response({"error": "Failed to fetch data from Google Maps API"}, status=response.status_code)
        data = response.json()
        if 'results' not in data:
            return Response({"error": "No results found"}, status=404)
        results = data['results']
        return Response(results, status=200)
