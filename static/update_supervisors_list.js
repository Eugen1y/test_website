$(document).ready(function () {
    // Функція для оновлення списку начальників
    function updateSupervisors() {
        var selectedLevel = $('#id_level').val();
        var url = '/ajax/supervisors/?level=' + selectedLevel;

        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $('#id_supervisor').empty();

                $.each(data, function (key, value) {
                    $('#id_supervisor').append($('<option>', {
                        value: value.id,
                        text: value.full_name
                    }));
                });
            },
            error: function (xhr, status, error) {
                console.error('Error updating supervisors:', error);
            }
        });
    }

    // Викликати функцію при завантаженні сторінки та при зміні рівня
    updateSupervisors();
    $('#id_level').change(updateSupervisors);
});
