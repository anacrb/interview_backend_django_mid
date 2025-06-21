from datetime import date
from typing import List

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.repository import DjangoOrderRepository
from interview.order.serializers import OrderSerializer, OrderTagSerializer
from interview.order.use_cases import GetOrdersByDateRangeUseCase


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

class OrderListByDateRangeView(APIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        start_date_str = request.query_params.get("start_date")
        embargo_date_str = request.query_params.get("embargo_date")

        if not start_date_str or not embargo_date_str:
            return Response(
                {"error": "Both 'start_date' and 'end_date' query parameters (YYYY-MM-DD) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_date_obj = date.fromisoformat(start_date_str)
            embargo_date_obj = date.fromisoformat(embargo_date_str)
        except ValueError as e:
            return Response(
                {"error": f"Invalid date format: {str(e)}. Please use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order_repo = DjangoOrderRepository()
        get_orders_use_case = GetOrdersByDateRangeUseCase(order_repo)

        try:
            orders: List[Order] = get_orders_use_case.execute(start_date_obj, embargo_date_obj)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )