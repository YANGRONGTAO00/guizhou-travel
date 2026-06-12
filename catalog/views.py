from django.contrib import messages
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView

from .forms import ScenicSpotForm
from .models import Feature, Region, ScenicSpot


class HomeView(TemplateView):
    template_name = "catalog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spot_count"] = ScenicSpot.objects.count()
        context["region_count"] = Region.objects.count()
        context["feature_count"] = Feature.objects.count()
        context["top_spots"] = (
            ScenicSpot.objects.select_related("region")
            .prefetch_related("features")
            .order_by("-rating", "name")[:3]
        )
        return context


class SpotListView(ListView):
    model = ScenicSpot
    template_name = "catalog/spot_list.html"
    context_object_name = "spots"
    paginate_by = 9

    def get_queryset(self):
        queryset = (
            ScenicSpot.objects.select_related("region")
            .prefetch_related("features")
            .order_by("name")
        )
        query = self.request.GET.get("q", "").strip()
        region = self.request.GET.get("region", "").strip()
        category = self.request.GET.get("category", "").strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(short_description__icontains=query)
                | Q(address__icontains=query)
            )
        if region:
            queryset = queryset.filter(region_id=region)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["regions"] = Region.objects.annotate(spot_total=Count("spots"))
        context["categories"] = ScenicSpot.Category.choices
        context["current_q"] = self.request.GET.get("q", "")
        context["current_region"] = self.request.GET.get("region", "")
        context["current_category"] = self.request.GET.get("category", "")
        return context


class SpotDetailView(DetailView):
    model = ScenicSpot
    template_name = "catalog/spot_detail.html"
    context_object_name = "spot"
    queryset = ScenicSpot.objects.select_related("region", "profile").prefetch_related("features")


class SpotCreateView(CreateView):
    model = ScenicSpot
    form_class = ScenicSpotForm
    template_name = "catalog/spot_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Новая достопримечательность успешно сохранена и сразу отображается в каталоге.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "В форме есть ошибки. Исправьте поля по подсказкам и отправьте ещё раз.")
        return super().form_invalid(form)


class SpotDeleteView(DeleteView):
    model = ScenicSpot
    template_name = "catalog/spot_confirm_delete.html"
    success_url = reverse_lazy("spot_list")
    context_object_name = "spot"

    def form_valid(self, form):
        messages.success(self.request, f"Достопримечательность удалена: {self.object.name}")
        return super().form_valid(form)
