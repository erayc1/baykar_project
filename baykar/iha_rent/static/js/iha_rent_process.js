function showIhaRentTable() {
    $('#ihaRentTableContainer').show();
    if (!$.fn.dataTable.isDataTable('#ihaRentlist')) {
        $('#ihaRentlist').DataTable({
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
                            <button type="button" class="btn btn-secondary" onclick="openDatePicker('${row.id}','${row.brand}', '${row.model}', '${row.category}', '${row.height}')">Add</button>
                        `;
                    }
                }
            ]
        });
    }
}

function openDatePicker(id,brand, model, category, height) {
    $('#datePickerModal').data('id', id).data('brand', brand)
                        .data('model', model)
                        .data('category', category)
                        .data('height', height)
                        .dialog({
                            modal: true,
                            width: 400,
                            height: 300
                        });
}

function userAddRentRecords() {
    var id = $('#datePickerModal').data('id');
    var brand = $('#datePickerModal').data('brand');
    var model = $('#datePickerModal').data('model');
    var category = $('#datePickerModal').data('category');
    var height = $('#datePickerModal').data('height');
    var startDate = $('#startDate').val();
    var endDate = $('#endDate').val();

    $('#datePickerModal').dialog('close');
    $.ajax({
        url: addRentRecord,
        type: 'POST',
        data: JSON.stringify({
            id: id,
            brand: brand,
            model: model,
            category: category,
            height: height,
            start_date: startDate,
            end_date: endDate
        }),
        contentType: 'application/json',
        success: function(response) {
            if (response.success) {
                alert(response.message);
                $('#userRentlist').DataTable().ajax.reload();
            } else {
                alert(response.message);
            }
        },
        error: function(response) {
            alert('An error occurred');
        }
    });
}

function addIhaToRent(brand, model, category, height) {
    // Burada IHA'yı kiralama işlemine eklemek için gerekli işlemleri yapabilirsiniz
    alert(`IHA eklendi: ${brand}, ${model}, ${category}, ${height}`);
}

function deleteRent(id) {
    if (confirm('Bu kaydı silmek istediğinizden emin misiniz?')) {
        $.ajax({
            url: deleteRentRecord,
            type: 'POST',
            data: JSON.stringify({ id: id }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    $('#userRentlist').DataTable().ajax.reload();
                } else {
                    alert(response.message);
                }
            },
            error: function(response) {
                alert('Bir hata oluştu.');
            }
        });
    }
}

function editRent(id, userId, ihaId, startDate, endDate) {
    $('#editRecordId').val(id);
    $('#editUserId').val(userId);
    $('#editStartDate').val(formatDateTime(startDate));
    $('#editEndDate').val(formatDateTime(endDate));
    
    // IHA combobox'ı doldurma
    $.ajax({
        url: getAllIhas,
        type: 'GET',
        success: function(response) {
            if (response.success) {
                var options = '';
                response.data.forEach(function(iha) {
                    var selected = iha.id == ihaId ? 'selected' : '';
                    options += `<option value="${iha.id}" ${selected}>${iha.brand} ${iha.model}</option>`;
                });
                $('#editIhaId').html(options);
            } else {
                alert('IHA verileri alınamadı.');
            }
        },
        error: function(response) {
            alert('IHA verileri alınamadı.');
        }
    });
    
    $('#editModal').dialog({
        modal: true,
        width: 400,
        height: 400
    });
}

function formatDateTime(dateTimeStr) {
    var date = new Date(dateTimeStr);
    var year = date.getFullYear();
    var month = ('0' + (date.getMonth() + 1)).slice(-2);
    var day = ('0' + date.getDate()).slice(-2);
    var hours = ('0' + date.getHours()).slice(-2);
    var minutes = ('0' + date.getMinutes()).slice(-2);
    var seconds = ('0' + date.getSeconds()).slice(-2);
    return year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds;
}


function saveEditRecord() {
    var id = $('#editRecordId').val();
    var userId = $('#editUserId').val();
    var ihaId = $('#editIhaId').val();
    var startDate = $('#editStartDate').val();
    var endDate = $('#editEndDate').val();

    $.ajax({
        url: updateRentRecordUrl,
        type: 'POST',
        data: JSON.stringify({
            id: id,
            user_id: userId,
            iha_id: ihaId,
            start_date: startDate,
            end_date: endDate
        }),
        contentType: 'application/json',
        success: function(response) {
            if (response.success) {
                alert(response.message);
                $('#editModal').dialog('close');
                $('#userRentlist').DataTable().ajax.reload();
            } else {
                alert(response.message);
            }
        },
        error: function(response) {
            alert('Bir hata oluştu.');
        }
    });
}

function editIha(id, brand, model, category, height) {
    $('#editIhaId').val(id);
    $('#editBrand').val(brand);
    $('#editModel').val(model);
    $('#editCategory').val(category);
    $('#editHeight').val(height);

    $('#editIhaModal').dialog({
        modal: true,
        width: 400,
        height: 400
    });
}

function saveEditIha() {
    var id = $('#editIhaId').val();
    var brand = $('#editBrand').val();
    var model = $('#editModel').val();
    var category = $('#editCategory').val();
    var height = $('#editHeight').val();

    $.ajax({
        url: updateIhaUrl,
        type: 'POST',
        data: JSON.stringify({
            id: id,
            brand: brand,
            model: model,
            category: category,
            height: height
        }),
        contentType: 'application/json',
        success: function(response) {
            if (response.success) {
                alert(response.message);
                $('#editIhaModal').dialog('close');
                $('#ihalist').DataTable().ajax.reload();
            } else {
                alert(response.message);
            }
        },
        error: function(response) {
            alert('Bir hata oluştu.');
        }
    });
}

function deleteIha(id) {
    if (confirm('Bu kaydı silmek istediğinizden emin misiniz?')) {
        $.ajax({
            url: deleteIhaUrl,
            type: 'POST',
            data: JSON.stringify({ id: id }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    $('#ihalist').DataTable().ajax.reload();
                } else {
                    alert(response.message);
                }
            },
            error: function(response) {
                alert('Bir hata oluştu.');
            }
        });
    }
}



function addIHA() {
    var brand = $('#brand').val();
    var model = $('#model').val();
    var category = $('#category').val();
    var height = $('#height').val();
    
    $.ajax({
        url: adminAddIhaApiUrl,
        type: 'POST',
        data: JSON.stringify({
            brand: brand,
            model: model,
            category: category,
            height: height
        }),
        contentType: 'application/json',
        success: function(response) {
            if (response.success) {
                alert(response.message);
                window.location.href = adminHomeUrl;
            } else {
                alert(response.message);
            }
        },
        error: function(response) {
            alert('An error occurred');
        }
    });
}