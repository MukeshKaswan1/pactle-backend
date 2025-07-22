from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import CartItem, Order
from .serializers import CartItemSerializer, OrderSerializer
from rest_framework.response import Response
from django.core.mail import send_mail
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
print("SLACK_BOT_TOKEN:", settings.SLACK_BOT_TOKEN)
print("SLACK_CHANNEL_ID:", settings.SLACK_CHANNEL_ID)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print('slack')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, status='PAID')
        # Clear the user's cart after order is placed
        CartItem.objects.filter(user=request.user).delete()
        # Send order confirmation email
        user_email = request.user.email
        if user_email:
            send_mail(
                subject='Order Confirmation',
                message=f'Thank you for your order #{serializer.data["id"]}! Your order has been placed successfully.',
                from_email=None,  # Use DEFAULT_FROM_EMAIL
                recipient_list=[user_email],
                fail_silently=True,
            )
        # Send Slack notification
        slack_token = getattr(settings, 'SLACK_BOT_TOKEN', None)
        slack_channel = getattr(settings, 'SLACK_CHANNEL_ID', None)
        if slack_token and slack_channel:
            slack_message = {
                "channel": slack_channel,
                "text": f":shopping_cart: New order {serializer.data['id']} for ${serializer.data['total_amount']} by {request.user.username}"
            }
            headers = {
                "Authorization": f"Bearer {slack_token}",
                "Content-Type": "application/json"
            }
            print("Sending Slack notification to", slack_channel)
            try:
                requests.post("https://slack.com/api/chat.postMessage", json=slack_message, headers=headers, timeout=5)
            except Exception as e:
                print(f"Slack notification failed: {e}")
        return Response(serializer.data, status=201)


class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            amount = int(float(request.data.get('amount', 0)) * 100)  # amount in cents
            if amount < 50:  # Stripe minimum is 50 cents for USD
                return Response({'error': 'Amount must be at least $0.50'}, status=400)
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                metadata={'user_id': request.user.id}
            )
            return Response({'clientSecret': intent.client_secret})
        except Exception as e:
            print("Stripe PaymentIntent error:", e)
            return Response({'error': str(e)}, status=500)