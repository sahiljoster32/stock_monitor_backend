## This folder contain scripts for users app.

users app basically defines functionally for users, like defining `WatchList` model, defining routes for login and registration, defining serializers for each url route method(or view).

 - apps.py -> Defines users app's configs.
 - serializers.py -> Defines serializers for users app's views.
 - test.py -> Contains tests related to users functionality, like login, logout behavior.
 - urls.py -> Defines urls for users app like `users/login`, and `user/register`.
 - views.py -> Contains all users app's views (or contains all methods that are bound to a particular api route.)
