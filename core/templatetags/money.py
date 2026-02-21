from django import template

register = template.Library()

@register.filter
def brl_from_cents(value):
    try:
        cents = int(value)
        reais = cents / 100
        # formata 1234.5 -> "1.234,50"
        s = f"{reais:,.2f}"
        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return value
