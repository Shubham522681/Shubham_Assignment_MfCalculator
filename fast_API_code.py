from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta

app = FastAPI()





def get_mutual_fund_data(scheme_code):

    pass

@app.get("/profit")
async def calculate_profit_route(
    scheme_code: str = Query(..., title="Mutual Fund Scheme Code"),
    start_date: Optional[str] = Query(..., title="Purchase Date (dd-mm-yyyy)"),
    end_date: Optional[str] = Query(..., title="Redemption Date (dd-mm-yyyy)"),
    capital: float = Query(1000000.0, title="Initial Investment Amount")
):
    try:
        # Use the MutualFundProfitCalculator class to calculate profit
        calculator = MutualFundProfitCalculator()

   
        data = get_mutual_fund_data(scheme_code)

      
        start_date = datetime.strptime(start_date, "%d-%m-%Y") if start_date else None
        end_date = datetime.strptime(end_date, "%d-%m-%Y") if end_date else None

        # If start_date is not present, use the next available date
        if start_date and start_date not in [entry['date'] for entry in data['data']]:
            start_date += timedelta(days=1)

        # If end_date is not present, use the previous available date
        if end_date and end_date not in [entry['date'] for entry in data['data']]:
            end_date -= timedelta(days=1)

        start_date_str = start_date.strftime("%d-%m-%Y") if start_date else None
        end_date_str = end_date.strftime("%d-%m-%Y") if end_date else None

        profit = calculator.calculate_profit(scheme_code, start_date_str, end_date_str, capital)

        if profit is not None:
            return {"net_profit": profit}
        else:
            raise HTTPException(status_code=500, detail="Unable to calculate net profit.")

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {ve}")
    except TypeError as te:
        raise HTTPException(status_code=400, detail=f"Type conversion error: {te}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

