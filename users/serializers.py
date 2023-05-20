"""
Module for defining the users app's serializers.
"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class LoginSerializer(serializers.Serializer):
    """
    Serializer class for user login.

    This serializer class ensures the validation of username and password
    which are provided by the user. Also, takes care of whether credentials
    provided are correct or not.

    Attributes:
        username: Field for the user's username.
        password: Field for the user's password.

    Methods:
        validate: Validates the username and password, and then validates
            the user if both fields are ok and provided.

    This serializer raises:
        ValidationError: Both "username" and "password" are required.
            - If one of the field from username and password is not present.
        ValidationError: Access denied: wrong username or password.
            - If either username or password is not correct.
    """

    username = serializers.CharField(
        label="Username",
        write_only=True,
        required=True
    )

    # Password is defined with {'input_type': 'password'} to hide the
    # entered password when api is used in the DRF browsable API.
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        required=True
    )


    def validate(self, attrs):
        """This method validates the user entered username and password
        against DB stored user objects using `authenticate` method.

        Args:
            attrs (Dict[str, Any]): A key-value pairs of received inputs.

        Returns:
            Dict[str, Any]: A validated key-value pairs of received inputs
            along with logged in user object.

        Raises:
            ValidationError: Access denied: wrong username or password.
            ValidationError: Both "username" and "password" are required.
        """

        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:

            # Trying to authenticate the user using user provided credentials.
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            if not user:
                # If user is not found with the given credentials then `user`
                # is assigned as None and this validation error will be raised.
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer class for user registration.

    This serializer handles the validation and creation of user registration
    data. It ensures that the password fields match and creates a new user
    with the provided information.

    Attributes:
        username: Field for the user's username.
        email: Field for the user's email address.
        password: Field for the user's password.
        password2: Field for confirming the user's password.

    Meta:
        model: The User model associated with the serializer.
        fields: The fields to include in the serialized representation.
        extra_kwargs: Additional keyword arguments for specific fields.

    Methods:
        validate: Validates the password fields to ensure they match.
        create: Creates a new user with the provided data.

    This serializer raises:
        ValidationError: Password fields didn't match.
            - If password and password2 didn't match.
    """

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)


    class Meta:
        """
        Class represents the meta information about RegisterSerializer, like
        which fields needs to include in the serialized representation, model
        associated with it and etc.

        Attributes:
            model: The User model associated with the serializer.
            fields: The fields to include in the serialized representation.
            extra_kwargs: Additional keyword arguments for specific fields.
        """
        model = User
        fields = (
            'username', 'password', 'password2', 'email', 'first_name',
            'last_name'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


    def validate(self, attrs):
        """This method matches the password and password2 against each
        other and raises error if both are not matching.

        Args:
            attrs (Dict[str, Any]): A key-value pairs of received inputs.

        Returns:
            Dict[str, Any]: A validated key-value pairs of received inputs.

        Raises:
            ValidationError: Password fields didn't match.
        """

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs


    def create(self, validated_data):
        """This method creates a new user with the provided validated data and
        saves it in the DB.

        Args:
            validated_data (Dict[str, Any]): A validated key-value pairs of
                received inputs.

        Returns:
            User (model instance): A newly created user model instance.
        """

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
