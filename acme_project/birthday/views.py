from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
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


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy("birthday:list")


class BirthdayFormMixin:
    form_class = BirthdayForm
    template_name = "birthday/birthday.html"


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    pass


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
    pass


class BirthdayDeleteView(BirthdayMixin, DeleteView):
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
    paginate_by = 2


def birthday_list(request):
    # Получаем все объекты модели Birthday из БД.
    birthdays = Birthday.objects.order_by("id")
    paginator = Paginator(birthdays, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Передаём их в контекст шаблона.
    context = {"page_obj": page_obj}
    return render(request, "birthday/birthday_list.html", context)


def birthday(request, pk=None):
    # Если в запросе указан pk (если получен запрос на редактирование объекта):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Birthday, pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    # Передаём в форму либо данные из запроса, либо None.
    # В случае редактирования прикрепляем объект модели.
    form = BirthdayForm(
        request.POST or None, files=request.FILES or None, instance=instance
    )
    # Остальной код без изменений.
    context = {"form": form}
    # Сохраняем данные, полученные из формы, и отправляем ответ:
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(form.cleaned_data["birthday"])
        context.update({"birthday_countdown": birthday_countdown})
    return render(request, "birthday/birthday.html", context)


def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {"form": form}
    # Если был получен POST-запрос...
    if request.method == "POST":
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect("birthday:list")
    # Если был получен GET-запрос — отображаем форму.
    return render(request, "birthday/birthday.html", context)
