from fastapi import HTTPException


class CarAPIException(HTTPException):
    def __init__(self, detail=None, status_code=500):
        self.status_code = status_code
        self.detail = detail or "An unexpected error occurred"
        super().__init__(status_code=self.status_code, detail=self.detail)


class CarNotFoundException(CarAPIException):
    def __init__(self, detail=None):
        super().__init__(detail=detail or "Car not found", status_code=404)


class CarAlreadyExistsException(CarAPIException):
    def __init__(self, detail=None):
        super().__init__(
            detail=detail or "A similar car listing already exists", status_code=409
        )


class InvalidCarIDException(CarAPIException):
    def __init__(self, detail=None):
        super().__init__(detail=detail or "Invalid car ID format", status_code=400)
