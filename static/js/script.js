$(document).ready(function () {

    $('form').on('submit', function (event) {
        // preventing default form action
        event.preventDefault();

        // ajax called to search country capital
        $.ajax({
            type: 'POST',
            url: '/capital',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                country: $("#country").val()
            }),
            success: function (response) {
                // removing alert and adding record to table
                $('.alert').fadeOut();
                $('#tbody').html('<tr><td>' + response[0]['Capital'] + '</td><td>' + response[0]['Country'] + '</td></tr>');
            },
            error: function (error) {
                // removing record from table and showing alert
                $('#tbody').html('');
                $('.alert').fadeIn();
            }
        });

    });
});