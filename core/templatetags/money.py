from django import template

register = template.Library()

@register.filter
def brl_from_cents(value):
    try:
        cents = int(value)
    except (TypeError, ValueError):
        return "R$ 0,00"

    reais = cents / 100
    return f"R$ {reais:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
