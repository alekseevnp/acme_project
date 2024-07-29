from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy
from .forms import BirthdayForm, CongratulationForm
from .models import Birthday
from .utils import calculate_birthday_countdown

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


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
        context['form'] = CongratulationForm()
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        # Возвращаем словарь контекста.
        return context


class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # По умолчанию этот класс 
    # выполняет запрос queryset = Birthday.objects.all(),
    # но мы его переопределим:
    queryset = Birthday.objects.prefetch_related('tags').select_related('author')
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = "id"
    # ...и даже настройки пагинации:
    paginate_by = 10


@login_required
def add_comment(request, pk):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    birthday = get_object_or_404(Birthday, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        congratulation.author = request.user
        # В поле birthday передаём объект дня рождения.
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk) 