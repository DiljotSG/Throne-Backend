class Location:
    def __init__(
        self,
        latitude: float,
        longitude: float
    ) -> None:
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def verify(latitude: float, longitude: float) -> bool:
        return latitude <= 90 and latitude >= -90 and \
            longitude <= 180 and longitude >= -180

    def to_dict(self) -> dict:
        return self.__dict__.copy()
