<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Утилиты родителя для онлайн школы foxford</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
</head>

<body>

    <div class="container">
        <div class="row">
            <div class="col-lg-12">
                <h2>Генерация календаря</h2>
                <p>С помощью этой формы, вы можете получить ссылку для импорта календаря вашего ребенка в сторонний
                    инструмент
                    для календарей, например в Google календарь, календарь MacOS/Windows/Android/iOS/...</p>
                <p>Использование стороннего календаря, позволит вам настроить уведомления о уроках на ваших устройствах
                </p>
                <p>Войдите в ваш личный кабинет с учетной записью ребенка и зайдите на страницу <a
                        href="https://foxford.ru/elementary/dashboard/progress" target="_blank">Успеваемость за
                        неделю</a>
                </p>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-6">
                <input type="text" class="form-control" id="shared_calendar"
                    placeholder="https://foxford.ru/dashboard/shared_calendar/8917761/f58b27c809e5e45f91b78871cf51da0799899a1e">
                <div class="invalid-feedback">
                    введена неверная ссылка
                </div>
            </div>
            <div class="col-lg-6">
                <div class="input-group">
                    <input readonly type="text" id="ical_link" class="form-control"
                        placeholder="Тут будет ваша ссылка на календарь">
                    <button class="btn btn-success" type="button" id="copy_ical_link">Скопировать</button>
                </div>
            </div>
        </div>

    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8"
        crossorigin="anonymous"></script>
    <script src="https://code.jquery.com/jquery-3.6.1.min.js"
        integrity="sha256-o88AwQnZB+VDvE9tvIXrMQaPlFFSUTR+nldQm1LuPXQ=" crossorigin="anonymous"></script>

    <script lang="js">
        $(function () {
            $('#copy_ical_link').prop("disabled", true);

            $("#shared_calendar").on('input', function (e) {
                $('#shared_calendar').removeClass('is-invalid');
                $('#copy_ical_link').prop("disabled", true);

                let validatePattern = /https\:\/\/foxford\.ru\/dashboard\/shared_calendar\/[0-9]+\/[a-z0-9]+$/;
                let val = $("#shared_calendar").val();
                let valid = validatePattern.test(val);

                if (!valid) {
                    $('#shared_calendar').addClass('is-invalid');
                } else {
                    $('#copy_ical_link').prop("disabled", false);
                    let getPattern = /https\:\/\/foxford\.ru\/dashboard\/shared_calendar\/([0-9]+)\/([a-z0-9]+)$/;
                    let data = val.match(getPattern);
                    let user_id = data[1]
                    let token = data[2]

                    let ical_url = window.location.origin + '/ical/' + user_id + '/' + token
                    $('#ical_link').val(ical_url)
                }
            });

            $('#copy_ical_link').click(function () {
                let ical_url = $('#ical_link').val()
                navigator.clipboard.writeText(ical_url)
            });
        })
    </script>
</body>

</html>