from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy
from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


class BirthdayCreateView(CreateView):
    model = Birthday
    form_class = BirthdayForm
    pass


class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm
    pass


class BirthdayDeleteView(DeleteView):
    model = Birthday    
    success_url = reverse_lazy('birthday:list')
    pass


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context["birthday_countdown"] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context


class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = "id"
    # ...и даже настройки пагинации:
    paginate_by = 10
