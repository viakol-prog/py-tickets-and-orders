from django.db import transaction
from db.models import Order, Ticket
from django.db.models import QuerySet
from typing import Optional
from django.contrib.auth import get_user_model
from datetime import datetime


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: Optional[str] = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    if date:
        Order._meta.get_field("created_at").auto_now_add = False
        order = Order.objects.create(
            user=user,
            created_at=datetime.strptime(date, "%Y-%m-%d %H:%M")
        )
        Order._meta.get_field("created_at").auto_now_add = True
    else:
        order = Order.objects.create(user=user)

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"]
        )

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
