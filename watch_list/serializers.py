"""
Module for defining the watch_list app's serializers.
"""

from rest_framework import serializers


class WatchListSymbolSerializer(serializers.Serializer):
    """
    Serializer class for validating watch list symbols.

    This serializer is used to validate the symbols provided for a watch list.
    It ensures that the symbols meet the specified criteria. Like below:
        1. Length of symbols must be less or equals to 5.
            Note: This restriction is due to the free api usage
                  of alpha avantage. Alpha avantage can only serve
                  5 calls per minute and due to this we can only allow
                  max 5 calls in a minute per user.
        2. All values of symbols list must be string.

    Attributes:
        symbols: A list of watch list symbols.

    Methods:
        validate: Validates the symbols list for their length and
            values type.

    This serializer raises:
        ValidationError: Only limit of 5 symbols is allowed due to free
                         subscription of `alpha avantage`
            - If length of symbols list is more than 5.
        ValidationError: symbols must be a string value.
            - If any of the symbol is not of python string type.
    """

    symbols = serializers.ListField(
        label='Watch List Symbols', write_only=True
    )


    def validate(self, attrs):
        """This method validates the watch list symbols based on the
        following criteria:
        - The number of symbols should not exceed 5.
        - Each symbol should be a string.

        Args:
            attrs (Dict[str, Any]): A key-value pairs of received inputs.

        Returns:
            Dict[str, Any]: A validated key-value pairs of received inputs.

        Raises:
            ValidationError: Only limit of 5 symbols is allowed due to
                free subscription of `alpha avantage`.
            ValidationError: symbols must be a string value.
        """

        symbols = attrs.get('symbols')

        if len(symbols) > 5:
            msg = (
                "Only limit of 5 symbols is allowed due to " +
                "free subscription of `alpha avantage`."
            )
            raise serializers.ValidationError(msg)

        for symbol in symbols:
            if not isinstance(symbol, str):
                msg = "symbols must be a string value."
                raise serializers.ValidationError(msg)

        return attrs
