

$(document).ready(function() {
    // Kullanıcılar DataTable
    if (!$.fn.dataTable.isDataTable('#userlist')) {
        $('#userlist').DataTable({
            "processing": true,
            "serverSide": true,
            "ajax": {
                "url": usersDataUrl,
                "type": "POST",
                "data": function(d) {
                    d.csrfmiddlewaretoken = csrfToken;
                }
            },
            "columns": [
                { "data": "email" },
                { "data": "name" },
                { "data": "surname" },
                { "data": "is_admin" }
            ]
        });
    
        // IHA DataTable
        $('#ihalist').DataTable({
            "processing": true,
            "serverSide": true,
            "ajax": {
                "url": ihaDataUrl,
                "type": "POST",
                "data": function(d) {
                    d.csrfmiddlewaretoken = csrfToken;
                }
            },
            "columns": [
                { "data": "brand" },
                { "data": "model" },
                { "data": "category" },
                { "data": "height" },
                {
                    "data": null,
                    "render": function(data, type, row) {
                        return `
                            <button type="button" class="btn btn-secondary" onclick="editIha('${row.id}', '${row.brand}', '${row.model}', '${row.category}', '${row.height}')">Edit</button>
                            <button type="button" class="btn btn-danger" onclick="deleteIha('${row.id}')">Delete</button>
                        `;
                    }
                }
            ]
        });
    }

    if (!$.fn.dataTable.isDataTable('#ihalist')) {
        $('#ihalist').DataTable({
            "processing": true,
            "serverSide": true,
            "ajax": {
                "url": ihaDataUrl,
                "type": "POST",
                "data": function(d) {
                    d.csrfmiddlewaretoken = csrfToken;
                }
            },
            "columns": [
                { "data": "brand" },
                { "data": "model" },
                { "data": "category" },
                { "data": "height" }
            ]
        });
    }

    if (!$.fn.dataTable.isDataTable('#rentlist')) {
        $(".datetimepicker").datetimepicker({
            dateFormat: 'yy-mm-dd',
            timeFormat: 'HH:mm:ss'
        });
        $('#rentlist').DataTable({
            "processing": true,
            "serverSide": true,
            "ajax": {
                "url": rentDataUrl,
                "type": "POST",
                "data": function(d) {
                    d.csrfmiddlewaretoken = csrfToken;
                }
            },
            "columns": [
                { "data": "brand" },
                { "data": "model" },
                { "data": "start_date" },
                { "data": "end_date" },
                
            ]
        });
    }

    if (!$.fn.dataTable.isDataTable('#userRentlist')) {
        $(".datetimepicker").datetimepicker({
            dateFormat: 'yy-mm-dd',
            timeFormat: 'HH:mm:ss'
        });

        $('#userRentlist').DataTable({
            "processing": true,
            "serverSide": true,
            "ajax": {
                "url": userRentDataUrl,
                "type": "POST",
                "data": function(d) {
                    d.csrfmiddlewaretoken = csrfToken;
                },
                "error": function(xhr, error, thrown) {
                    if (xhr.responseJSON && xhr.responseJSON.message === 'User not logged in') {
                        window.location.href = '/login';
                    } else {
                        alert('Bir hata oluştu: ' + thrown);
                    }
                }
            },
            "columns": [
                { "data": "brand" },
                { "data": "model" },
                { "data": "start_date" },
                { "data": "end_date" },
                {
                    "data": null,
                    "render": function(data, type, row) {
                        return `
                            <button type="button" class="btn btn-secondary" onclick="editRent('${row.id}', '${row.user_id}', '${row.iha_id}', '${row.start_date}', '${row.end_date}')">Edit</button>
                            <button type="button" class="btn btn-secondary" onclick="deleteRent('${row.id}')">Delete</button>
                        `;
                    }
                }
            ]
        });
   
    }
        
});

