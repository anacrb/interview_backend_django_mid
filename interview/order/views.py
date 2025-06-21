from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.repository import DjangoOrderRepository
from interview.order.serializers import OrderSerializer, OrderTagSerializer
from interview.order.use_cases import DeactivateOrderUseCase


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

class DeactivateOrderView(APIView):

    def patch(self, request: Request, id: int, *args, **kwargs) -> Response:
        order_repo = DjangoOrderRepository()
        deactivate_order_use_case = DeactivateOrderUseCase(order_repo)

        try:
            deactivated_order = deactivate_order_use_case.execute(id)

            if deactivated_order:
                serializer = OrderSerializer(deactivated_order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": f"Order with ID {id} not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
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