# Future Improvements for the Backend

Below are a list of improvements for the Backend that should be implemented in the future should the project continue to be developed.

- [ ] Support for filtering buildings by amenity.
- [ ] Support for filtering washrooms by gender.
- [ ] Support for deleting reviews.
- [ ] Support for editing washrooms.
- [ ] Support for deleting washrooms.
- [ ] Support for deleting users.
- [ ] Support for adding buildings through the API / Support for fetching buildings from an external map service.
- [ ] Make newly added washrooms go through a verification process before being visible within the application.
- [ ] Separate the database persistence logic to a separate server that handles DB *update* requests sequentially, doing so will eliminate possible concurrency issues when doing DB update requests directly in the Lambda. Reading from the DB doesn't create any race conditions so the reading logic can remain in the Lambda without any concern.
- [ ] Restructure persistence logic to fetch all required attributes with one SQL call, for example, fetching a washroom returns the `Building Title`, the `Amenities` and `Ratings` for that particular washroom. Currently, we fetch this information by making additional SQL calls for each washroom. For a single washroom this method is fine but it does not scale well when asking for all washrooms. We should redesign our persistence layer to use more advanced SQL calls, such as Table Joins, in order to retrieve this data in a single call, thereby reducing the latency in the Backend when fetching Washrooms and Buildings.
- [ ] Separate the development dependencies from `requirements.txt`. Currently our requirements file includes all the dependencies for the application including dependencies that are necessary for development but not for running the application (flake8, tox, etc.). These dependencies should be put into a separate list so that the deployed Lambda package can be smaller and only contain the dependencies it needs to run the application.
- [ ] Create better stubs/fakes that support the exact same set of features as the implementation persistence layer. The stubs should be robust and use a dictionary as the primitive data structure underneath to support more advanced operations more robustly. Additionally, amenity filtering should also be supported.
- [ ] Create unit tests for individual helper functions within the application to increase code coverage (rather than just having integration tests for the API endpoints).
- [ ] Find a way to test the database persistence within the integration tests. This would require creating a local mySQL database and testing the persistence layer on that.
- [ ] Add support for filtering all washrooms by default across the application based on user profile settings (e.g. only accessible and female washrooms, etc).
- [ ] Add better logging to see detailed information on the incoming requests (from clients) and outgoing requests (to database) (e.g. "Request made to `/washrooms`. Fetching 50 washrooms and expanding with Building Title, Amenities, and Ratings. Completed operation in 800ms"). This will allow us to further improve Backend performance when issues arise.
