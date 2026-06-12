from django import forms

from .models import ScenicSpot, SpotProfile


class ScenicSpotForm(forms.ModelForm):
    best_season = forms.CharField(
        label="Лучший сезон для поездки",
        max_length=80,
        help_text="Например: апрель–октябрь, лето, весна и осень",
    )
    suggested_hours = forms.IntegerField(
        label="Рекомендуемое время посещения, часы",
        min_value=1,
        max_value=72,
        initial=4,
    )
    transport_tips = forms.CharField(
        label="Советы по транспорту",
        widget=forms.Textarea(attrs={"rows": 3}),
    )
    official_phone = forms.CharField(
        label="Телефон для справок",
        required=False,
        max_length=30,
    )

    class Meta:
        model = ScenicSpot
        fields = [
            "name",
            "region",
            "features",
            "category",
            "short_description",
            "address",
            "ticket_price",
            "rating",
            "opening_date",
            "is_world_heritage",
            "image_url",
        ]
        widgets = {
            "opening_date": forms.DateInput(attrs={"type": "date"}),
            "short_description": forms.Textarea(attrs={"rows": 4}),
            "features": forms.CheckboxSelectMultiple,
        }
        help_texts = {
            "ticket_price": "Для бесплатного входа укажите 0.",
            "rating": "Введите целое число от 1 до 5.",
            "image_url": "Необязательно; если поле пустое, будет показан стандартный градиент.",
        }

    def clean_ticket_price(self):
        price = self.cleaned_data["ticket_price"]
        if price < 0:
            raise forms.ValidationError("Цена билета не может быть отрицательной.")
        return price

    def clean_short_description(self):
        text = self.cleaned_data["short_description"].strip()
        if len(text) < 12:
            raise forms.ValidationError("Описание должно содержать не менее 12 символов.")
        return text

    def save(self, commit=True):
        spot = super().save(commit=commit)
        if commit:
            SpotProfile.objects.update_or_create(
                spot=spot,
                defaults={
                    "best_season": self.cleaned_data["best_season"],
                    "suggested_hours": self.cleaned_data["suggested_hours"],
                    "transport_tips": self.cleaned_data["transport_tips"],
                    "official_phone": self.cleaned_data["official_phone"],
                },
            )
            self.save_m2m()
        return spot
