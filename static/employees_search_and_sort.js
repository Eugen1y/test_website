    $(document).ready(function () {
      $('#employee-sort-form').submit(function (event) {
        event.preventDefault();
        var form = $(this);
        $.ajax({
          type: form.attr('method'),
          url: form.attr('action'),
          data: form.serialize(),
          success: function (data) {
            $('#employee-list').html(data.html);
          }
        });
      });
    });

    function loadEmployeeList(searchQuery) {
      $.ajax({
        type: 'GET',
        url: '{% url "load_employee_list" %}',
        data: { search_query: searchQuery },
        success: function (data) {

        }
      });
    }


