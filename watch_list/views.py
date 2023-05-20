"""
Module for defining views of watch_list app. It can be
function based or class based.
"""

from rest_framework import generics, permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import WatchListSymbolSerializer

from .wrapper import symbols_data_fetcher


class FetchSymbolsData(APIView):
    """
    API view for retrieving data for a list of symbols.

    This view requires authentication and token-based authentication
    is used. It retrieves the latest data and graph data for the symbols
    provided in the request. Currently, graph data is formatted for candle
    stick graph data. Note:
        1. If any of the symbols is not a valid symbol or the data is not
            available for that symbol from alpha avantage, then that symbol
            is excluded from response and response only include those
            symbols that has data.
        2. If 6th request is made in a single minute then function immediately
            throws an error with status code 429 without any response.

    Attributes:
        permission_classes: Specifies the permission for users, currently
            it is set to `(permissions.IsAuthenticated,)`, requiring the
            user to be authenticated.
        authentication_classes: The authentication class used for authenticating
            the user. Currently, it is set to `(authentication.TokenAuthentication,)`,
            using token-based authentication.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)


    def post(self, request, *args, **kwargs):
        """Handles the POST request for retrieving data for a list of symbols.
        Also, validates the input data, retrieves the data for the symbols,
        and updates the user's watchlist symbols with the retrieved data.
        
        In response, it sends the latest data and graph data for each valid symbol
        along with meta information like value names (open, close, and etc.) and
        symbol list for which this data is fetched.

        Args:
            request (Request): A Django request object.
            *args: Additional named arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: Response object containing the latest data and
            graph data(candle stick) along with fetched and valid symbol list.
        """
        serializer = WatchListSymbolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        symbols = serializer.validated_data['symbols']
        user = request.user

        response = (
            symbols_data_fetcher.get_symbols_latest_and_graph_data(symbols)
        )

        # Throwing error when we have reached the 5 calls per minute limit.
        if 'Note' in response and 'reached the limit' in response['Note']:
            return Response(response, status=429)

        user.watchlist.symbols = response['symbols']
        user.save()

        return Response(response)
