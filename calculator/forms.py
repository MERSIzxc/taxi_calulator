from django import forms


class TaxiCalculatorForm(forms.Form):
    weekly_brutto = forms.DecimalField(
        label='Доход за неделю (брутто), zł',
        min_value=0,
        decimal_places=2,
        max_digits=12,
        initial=2000,
    )
    partner_fixed = forms.DecimalField(
        label='Партнёрка zł',
        min_value=0,
        decimal_places=2,
        max_digits=12,
        initial=60,
    )
    zus_fixed = forms.DecimalField(
        label='ZUS zł',
        min_value=0,
        decimal_places=2,
        max_digits=12,
        initial=60,
    )
    vat_percent = forms.DecimalField(
        label='VAT, % от брутто',
        min_value=0,
        max_value=100,
        decimal_places=2,
        max_digits=5,
        initial=6,
    )
    ryczalt_percent = forms.DecimalField(
        label='Ryczałt, % от нетто (после партнёрки, ZUS и VAT)',
        min_value=0,
        max_value=100,
        decimal_places=2,
        max_digits=5,
        initial=8.5,
    )
    km_week = forms.DecimalField(
        label='Километраж за неделю, км',
        min_value=0,
        decimal_places=2,
        max_digits=10,
        initial=1100,
    )
    liters_per_100km = forms.DecimalField(
        label='Расход, л на 100 км',
        min_value=0,
        decimal_places=2,
        max_digits=6,
        initial=7,
    )
    gas_price_per_l = forms.DecimalField(
        label='Цена газа за литр, zł',
        min_value=0,
        decimal_places=2,
        max_digits=8,
        initial=3.80,
    )
    insurance_yearly = forms.DecimalField(
        label='Страховка в год, zł',
        min_value=0,
        decimal_places=2,
        max_digits=12,
        initial=6600,
    )
    oil_per_10k_km = forms.DecimalField(
        label='Замена масла: zł на 10 000 км',
        min_value=0,
        decimal_places=2,
        max_digits=12,
        initial=400,
    )
    amort_per_10k_km = forms.DecimalField(
        label='Амортизация и ремонты: zł на 10 000 км',
        min_value=0,
        decimal_places=2,
        max_digits=12,
        initial=1000,
    )
    hours_week = forms.DecimalField(
        label='Часы работы за неделю',
        min_value=0,
        decimal_places=2,
        max_digits=7,
        initial=50,
    )

    def cleaned_decimal(self, name: str) -> float:
        value = self.cleaned_data.get(name)
        return float(value) if value is not None else 0.0
