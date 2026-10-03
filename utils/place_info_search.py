import os
import json
from langchain_tavily import TavilySearch
import requests


class GooglePlaceSearchTool:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://places.googleapis.com/v1/places:searchText"

        if not self.api_key:
            raise ValueError("GPLACES_API_KEY is not set.")

        print("Google Places API (New) is ready")

    def _search(self, query: str):
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": (
                "places.displayName,"
                "places.formattedAddress,"
                "places.rating,"
                "places.userRatingCount,"
                "places.types"
            )
        }

        response = requests.post(
            self.url,
            headers=headers,
            json={
                "textQuery": query,
                "pageSize": 10
            },
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for place in data.get("places", []):
            results.append({
                "name": place.get("displayName", {}).get("text"),
                "address": place.get("formattedAddress"),
                "rating": place.get("rating"),
                "user_rating_count": place.get("userRatingCount"),
                "types": place.get("types", [])
            })

        return results

    def google_search_attraction(self, place: str):
        """
        Searches for attractions in the specified place using GooglePlaces API.
        """

        return self._search(
            f"top attractions in and around {place}"
        )

    def google_search_restaurants(self, place: str):
        """
        Searches for restaurants in the specified place using GooglePlaces API."""
        return self._search(
            f"top 10 restaurants and eateries in and around {place}"
        )

    def google_search_activity(self, place: str):
        """
        Searches for popular activities in the specified place using GooglePlaces API."""
        return self._search(
            f"popular activities and things to do in {place}"
        )

    def google_search_transportation(self, place: str):
        """
        Searches for available modes of transportation in the specified place using GooglePlaces API.
        """
        return self._search(
            f"transportation options and transit stations in {place}"
        )

    
class TavilyPlaceSearchTool:
    def __init__(self):
        print("TavilyPlacesearch tool are calling")

    def tavily_search_attractions(self, place: str) -> dict:
        """
        Searches for attraction in the specified place using TavilySearch.
        """    

        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query":f"top attractive places in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_restaurants(self, place:str) -> dict:
        """
        Searches for available restaurants in the specified place using TavilySearch.
        """

        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query":f"what are the top 10 restaurants and eateries in the around"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_activity(self, place: str) -> dict:
        """
        Searches for popular activities in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"activities in and around {place}"})
        if isinstance(result, dict) and result.get("asnwer"):
            return result["asnwer"]
        return result

    def tavily_search_transportation(self, place: str) -> dict:
        """
        Searches for available modes of transportation in the specified place using Tavilysearch
        """

        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({'query':f"What are the different modes of transportations available in {place}"})
        if isinstance(result, dict) and result.get("asnwer"):
            return result['answer']
        return result