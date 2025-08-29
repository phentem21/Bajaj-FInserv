from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Any
import re

app = FastAPI(
    title="Data Processing API",
    description="An API to process an array of data and return structured information.",
    version="1.0.0"
)

class RequestData(BaseModel):
    data: List[Any] = Field(..., example=["a", "1", "334", "4", "R", "$"])

class ResponseData(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    odd_numbers: List[str]
    even_numbers: List[str]
    alphabets: List[str]
    special_characters: List[str]
    sum: str
    concat_string: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Data Processing API. Use the /bfhl endpoint with a POST request."}

@app.post("/bfhl", response_model=ResponseData, status_code=status.HTTP_200_OK)
async def process_data(request: RequestData):
    try:
        odd_numbers = []
        even_numbers = []
        alphabets = []
        special_characters = []
        total_sum = 0
        concat_chars = []

        for item in request.data:
            item_str = str(item)
            if re.fullmatch(r'-?\d+', item_str):
                num = int(item_str)
                total_sum += num
                if num % 2 == 0:
                    even_numbers.append(item_str)
                else:
                    odd_numbers.append(item_str)
            elif item_str.isalpha():
                alphabets.append(item_str.upper())
                concat_chars.extend(list(item_str))
            else:
                special_characters.append(item_str)

        reversed_chars = concat_chars[::-1]
        concat_string = ""
        for i, char in enumerate(reversed_chars):
            if i % 2 == 0:
                concat_string += char.upper()
            else:
                concat_string += char.lower()

        user_id = "prakhar_malviya_21052004"
        email = "prakharmalviya.2105@gmail.com"
        roll_number = "22BCE10459"

        response_data = {
            "is_success": True,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": str(total_sum),
            "concat_string": concat_string,
        }
        return response_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal server error occurred: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)