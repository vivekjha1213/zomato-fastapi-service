from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import os

router = APIRouter()

data_path = os.path.join(os.path.dirname(__file__), 'Zomato data .csv')


def load_data():
    try:
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        # Log the error message or print it for debugging
        print(f"Error loading data: {e}")
        raise HTTPException(status_code=500, detail="Error loading data")


@router.get("/most_popular_restaurant_type/")
async def most_popular_restaurant_type():
    try:
        df = load_data()
        most_common_type = df['restaurant_type'].mode()[0]
        return {"most_popular_restaurant_type": most_common_type}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/votes_by_restaurant_type/")
async def votes_by_restaurant_type():
    try:
        df = load_data()
        votes_count = df.groupby('restaurant_type')['votes'].sum().to_dict()
        return JSONResponse(content=votes_count)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/most_common_rating/")
async def most_common_rating():
    try:
        df = load_data()
        most_common_rating = df['rating'].mode()[0]
        return {"most_common_rating": most_common_rating}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/average_spending_online/")
async def average_spending_online():
    try:
        df = load_data()
        online_orders = df[df['online_order'] == 'Yes']
        avg_spending = online_orders['spending'].mean()
        return {"average_spending_online": avg_spending}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/highest_rating_mode/")
async def highest_rating_mode():
    try:
        df = load_data()
        avg_rating_by_mode = df.groupby('online_order')['rating'].mean()
        highest_mode = avg_rating_by_mode.idxmax()
        return {"highest_rating_mode": highest_mode}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/type_restaurants_more_offline_orders/")
async def type_restaurants_more_offline_orders():
    try:
        df = load_data()
        offline_orders = df[df['online_order'] == 'No']
        type_offline_orders = offline_orders.groupby('restaurant_type').size()
        max_type = type_offline_orders.idxmax()
        return {"type_with_most_offline_orders": max_type}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
