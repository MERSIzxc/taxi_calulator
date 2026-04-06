from django.shortcuts import render

from .forms import TaxiCalculatorForm

WEEKS_PER_YEAR = 52


def taxi_calculator_view(request):
    result = None
    form = TaxiCalculatorForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        brutto = form.cleaned_decimal('weekly_brutto')
        partner = form.cleaned_decimal('partner_fixed')
        zus = form.cleaned_decimal('zus_fixed')
        vat_pct = form.cleaned_decimal('vat_percent')
        ryczalt_pct = form.cleaned_decimal('ryczalt_percent')
        km = form.cleaned_decimal('km_week')
        l_per_100 = form.cleaned_decimal('liters_per_100km')
        gas_price = form.cleaned_decimal('gas_price_per_l')
        insurance_year = form.cleaned_decimal('insurance_yearly')
        oil_10k = form.cleaned_decimal('oil_per_10k_km')
        amort_10k = form.cleaned_decimal('amort_per_10k_km')
        hours_week = form.cleaned_decimal('hours_week')

        vat_amount = brutto * (vat_pct / 100.0)
        netto_after_partner_zus_vat = brutto - partner - zus - vat_amount
        ryczalt_amount = max(netto_after_partner_zus_vat, 0) * (ryczalt_pct / 100.0)
        after_taxes = netto_after_partner_zus_vat - ryczalt_amount

        liters = km * (l_per_100 / 100.0)
        fuel_cost = liters * gas_price
        insurance_week = insurance_year / WEEKS_PER_YEAR
        oil_week = (oil_10k / 10000.0) * km
        amort_week = (amort_10k / 10000.0) * km

        operating_total = fuel_cost + insurance_week + oil_week + amort_week
        net_profit = after_taxes - operating_total
        total_expenses = partner + zus + vat_amount + ryczalt_amount + operating_total
        income_per_hour = net_profit / hours_week if hours_week > 0 else 0.0
        chart_total = max(brutto, total_expenses + max(net_profit, 0.0), 1.0)

        raw_expenses = [
            ("Партнерка", partner),
            ("ZUS", zus),
            ("VAT", vat_amount),
            ("Ryczałt", ryczalt_amount),
            ("Топливо", fuel_cost),
            ("Страховка", insurance_week),
            ("Масло", oil_week),
            ("Амортизация", amort_week),
        ]
        raw_expenses.sort(key=lambda item: item[1])
        max_expense_value = max((value for _, value in raw_expenses), default=1.0)
        expense_segments = []
        for label, value in raw_expenses:
            intensity = value / max_expense_value if max_expense_value > 0 else 0.0
            hue = 50 - (50 * intensity)  # 50=yellow, 0=red
            expense_segments.append(
                {
                    "label": label,
                    "value": value,
                    "width_percent": (value / chart_total) * 100.0,
                    "color": f"hsl({hue:.0f}, 95%, 54%)",
                }
            )

        profit_segment_percent = (max(net_profit, 0.0) / chart_total) * 100.0

        result = {
            'brutto': brutto,
            'partner': partner,
            'zus': zus,
            'vat_pct': vat_pct,
            'vat_amount': vat_amount,
            'netto_after_partner_zus_vat': netto_after_partner_zus_vat,
            'ryczalt_pct': ryczalt_pct,
            'ryczalt_amount': ryczalt_amount,
            'after_taxes': after_taxes,
            'km': km,
            'liters': liters,
            'fuel_cost': fuel_cost,
            'insurance_week': insurance_week,
            'oil_week': oil_week,
            'amort_week': amort_week,
            'operating_total': operating_total,
            'net_profit': net_profit,
            'hours_week': hours_week,
            'income_per_hour': income_per_hour,
            'total_expenses': total_expenses,
            'profit_segment_percent': profit_segment_percent,
            'expense_segments': expense_segments,
        }

    return render(
        request,
        'calculator/index.html',
        {
            'form': form,
            'result': result,
        },
    )
