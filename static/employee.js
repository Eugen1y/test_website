$(document).ready(function() {
    // Обработчик клика для существующих и новых сотрудников
    $('body').on('click', 'span.employee', function() {
        var employeeId = $(this).data('employee-id');
        var clickedEmployee = $(this);
        var subordinatesContainer = clickedEmployee.parent(); // Используем родительский контейнер

        // Проверяем, видимы ли подчиненные элементы
        var subordinatesVisible = subordinatesContainer.find('.subordinates-container').is(':visible');

        if (subordinatesVisible) {
            // Если видимы, скрываем их
            subordinatesContainer.find('.subordinates-container').hide();
        } else {
            // В противном случае, загружаем и показываем подчиненные элементы
            $.ajax({
                url: '/load_hierarchy/' + employeeId + '/',
                type: 'GET',
                dataType: 'json',
                success: function(data) {
                    renderSubordinates(data, subordinatesContainer, 10);

                    // Показываем подчиненные элементы
                    subordinatesContainer.find('.subordinates-container').show();
                },
                error: function(error) {
                    console.log('Помилка при завантаженні ієрархії: ' + error);
                }
            });
        }
    });

    function renderSubordinates(subordinateData, parentContainer, indentation) {
        // Удаляем старые подчиненные элементы перед обновлением
        parentContainer.find('.subordinates-container').remove();

        var subordinatesContainer = $('<div class="subordinates-container"></div>');
        subordinatesContainer.css('margin-left', indentation + 'px');
        parentContainer.append(subordinatesContainer);

        $.each(subordinateData.subordinates, function(index, subordinate) {
            var subordinateElement = $('<div><span class="employee" data-employee-id="' + subordinate.id + '">' + subordinate.name + '(' + subordinate.subordinates_count +')'+ '</span></div>');
            subordinateElement.css('margin-left', indentation + 'px');

            subordinatesContainer.append(subordinateElement);

            renderSubordinates(subordinate, subordinateElement, indentation);
        });
    }
});
