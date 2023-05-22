## This folder contain scripts for watch_list app.

watch_list app defines functionality for a particular user's watch_list, functionality like `fetching data for all symbols in a watch_list`, validating watch_list symbols, handling Alpha avantage APIs errors (like 5 calls per min limit exceed).

 - apps.py -> Defines watch_list app's configs.
 - serializers.py -> Defines serializers for watch_list app's views.
 - test.py -> Contains tests related to watch_list app's functionality.
 - urls.py -> Defines urls for watch_list app like `watchList/symbols-data`.
 - views.py -> Contains all watch_list app's views (or contains all methods that are bound to a particular api route.)
