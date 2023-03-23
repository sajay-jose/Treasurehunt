var loaderIcon = '<i class="fa fa-spinner fa-pulse fa-fw"></i>';
var sectionLoader = '<div class="data-loader-block data-loader-30"><div class="loader-19 data-loader-30"></div></div>';
var amountIcon = '<i class="fa fa-inr"></i>';

$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});

initFetchDataLoader();

$(document).ready(function() {

    $("#select_all").on("click", function () {

        if (this.checked) {

            $(".manual_entry_cb").each(function () {

                this.checked = true;

            });

        } else {

            $(".manual_entry_cb").each(function () {

                this.checked = false;

            });

        }

    });



    $(".manual_entry_cb").on("click", function () {

        if (

            $(".manual_entry_cb:checked").length == $(".manual_entry_cb").length

        ) {

            $("#select_all").prop("checked", true);

        } else {

            $("#select_all").prop("checked", false);

        }

    });

    setTimeout(() => {
        $('#action-alert').remove();
    }, 4000)

    initMenuActive(); //Init menu active

    $(document).on('click', '[loader]', function() {
        initLoader(this);
    });

    $(document).on('click', '[clearForm]', function() {

        let formId = $(this).data('form');
        $(formId).get(0).reset()
    });

    $('#action-message .alert').not('.alert-important').delay(3000).fadeOut(350);

    $(document).on('click', '.delete-data', function() {
        let modelAttr = '#delete-prompt-modal';
        $(modelAttr + ' input[name=hidden_delete_id]').val('');
        $(modelAttr).modal('show');
        $(modelAttr + ' input[name=hidden_delete_id]').val($(this).data('url'))
    })

    $(document).on('click', '.close-delete', function() {
        let modelAttr = '#delete-prompt-modal';
        $(modelAttr + ' .delete-confirm-btn').attr('data-url', '');
    });

    $(document).on('click', '.delete-confirm-btn', function() {
        $(this).html('<i class="fa fa-spinner fa-pulse"></i> Please wait...');
        let modelAttr = '#delete-prompt-modal';
        PostData($(modelAttr + ' input[name=hidden_delete_id]').val(), '', 'DELETE')
            .then(response => {
                if (response.status === true) {
                    $(this).html('<i class="fa fa-trash-alt"></i> Delete');
                    if ($('.dataTable').length > 0) {
                        resetDataTable('.dataTable', 'datatable');
                    } else {
                        window.location.reload();
                    }
                    $('#delete-prompt-modal').modal('hide');
                    $(modelAttr + ' input[name=hidden_delete_id]').val('');
                    intiNotification(response.message, 'success');
                }
            })
            .catch(error => {
                intiNotification(error.responseJSON.message, 'danger');
                $(this).html('<i class="fa fa-trash-alt"></i> Delete');
            })
    });

    $(document).on('keyup', '.number-only', function() {
        $(this).inputFilter(function(value) {
            return /^\d*[.,]?\d{0,2}$/.test(value);
        });
    })

});

$("#multi_delete_form").submit(function(e) {
e.preventDefault();
}).validate({
    
rules: {
},
messages: {
},
submitHandler: function(form,event) 
{
    if($('.dataTable [name^="sel_ids"]:checked').length) 
    {
        swal({
            title: "Warning",
            text: 'Are you sure to delete selected ?  Associated data will be removed.',
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "CONFIRM",
            cancelButtonText: "CANCEL",
            closeOnConfirm: false,
            closeOnCancel: false
            },function(inputValue){
                
            if (inputValue===false)
            {
                var $form_parent = $("table");
                $form_parent.find('[name^="sel_ids"]').prop('checked', false);
                swal.close();
            } 
            else 
            {/*confirm*/
                swal.close();                        
                var $form = $('#multi_delete_form');
                $.each( $('.dataTable [name^="sel_ids"]:checked'), function() {
                    var $input = $('<input type="hidden" name="' + this.name + '" value="' + $(this).val() + '" checked />');
                    
                    $form.append($input);
                });
        
                $.ajax({
                    url: form.action,
                    type: form.method,
                    data: $(form).serialize(),
                    dataType: "json",
                    success: function(data) {
                        if(data.status == true)
                        {
                            
                            swal({
                                title: "Success", 
                                text: data.success, 
                                type: "success"
                                },
                                function(){ 
                                    oTable.ajax.reload();
                                }
                            );
                        }
                        else
                        {
                            swal({
                            title: "Warning", 
                            text: data.warning, 
                            type: "warning"
                            });
                        }
                    }
                });
            }
        });
    } 
    else 
    {
        swal({
            title: "Warning", 
            text: 'Please select atleast one checkbox', 
            type: "warning"
        });
    }
}
});
$("#multi_approve_form").submit(function(e) {
    e.preventDefault();
    }).validate({
        
    rules: {
    },
    messages: {
    },
    submitHandler: function(form,event) 
    {
        if($('.dataTable [name^="sel_ids"]:checked').length) 
        {
            swal({
                title: "Warning",
                text: 'Are you sure to approve selected ?  Associated user will be approved.',
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "CONFIRM",
                cancelButtonText: "CANCEL",
                closeOnConfirm: false,
                closeOnCancel: false
                },function(inputValue){
                    
                if (inputValue===false)
                {
                    var $form_parent = $("table");
                    $form_parent.find('[name^="sel_ids"]').prop('checked', false);
                    swal.close();
                } 
                else 
                {/*confirm*/
                    swal.close();                        
                    var $form = $('#multi_approve_form');
                    $.each( $('.dataTable [name^="sel_ids"]:checked'), function() {
                        var $input = $('<input type="hidden" name="' + this.name + '" value="' + $(this).val() + '" checked />');
                        
                        $form.append($input);
                    });
            
                    $.ajax({
                        url: form.action,
                        type: form.method,
                        data: $(form).serialize(),
                        dataType: "json",
                        success: function(data) {
                            if(data.status == true)
                            {
                                
                                swal({
                                    title: "Success", 
                                    text: data.success, 
                                    type: "success"
                                    },
                                    function(){ 
                                        oTable.ajax.reload();
                                    }
                                );
                            }
                            else
                            {
                                swal({
                                title: "Warning", 
                                text: data.warning, 
                                type: "warning"
                                });
                            }
                        }
                    });
                }
            });
        } 
        else 
        {
            swal({
                title: "Warning", 
                text: 'Please select atleast one checkbox', 
                type: "warning"
            });
        }
    }
});
$("#multi_close_form").submit(function(e) {
    e.preventDefault();
    }).validate({
        
    rules: {
    },
    messages: {
    },
    submitHandler: function(form,event) 
    {
        if($('.dataTable [name^="sel_ids"]:checked').length) 
        {
            swal({
                title: "Warning",
                text: 'Are you sure to close selected cases?  Only progressive cases will be closed.',
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "CONFIRM",
                cancelButtonText: "CANCEL",
                closeOnConfirm: false,
                closeOnCancel: false
                },function(inputValue){
                    
                if (inputValue===false)
                {
                    var $form_parent = $("table");
                    $form_parent.find('[name^="sel_ids"]').prop('checked', false);
                    swal.close();
                } 
                else 
                {/*confirm*/
                    swal.close();                        
                    var $form = $('#multi_close_form');
                    $.each( $('.dataTable [name^="sel_ids"]:checked'), function() {
                        var $input = $('<input type="hidden" name="' + this.name + '" value="' + $(this).val() + '" checked />');
                        
                        $form.append($input);
                    });
            
                    $.ajax({
                        url: form.action,
                        type: form.method,
                        data: $(form).serialize(),
                        dataType: "json",
                        success: function(data) {
                            console.log(data);
                            if(data.status == true)
                            {
                                
                                swal({
                                    title: "Success", 
                                    text: data.success, 
                                    type: "success"
                                    },
                                    function(){ 
                                        oTable.ajax.reload();
                                    }
                                );
                            }
                            else
                            {
                                swal({
                                title: "Warning", 
                                text: data.warning, 
                                type: "warning"
                                });
                            }
                        }
                    });
                }
            });
        } 
        else 
        {
            swal({
                title: "Warning", 
                text: 'Please select atleast one checkbox', 
                type: "warning"
            });
        }
    }
});

$("#multi_progress_form").submit(function(e) {
    e.preventDefault();
    }).validate({
        
    rules: {
    },
    messages: {
    },
    submitHandler: function(form,event) 
    {
        if($('.dataTable [name^="sel_ids"]:checked').length) 
        {
            swal({
                title: "Warning",
                text: 'Are you sure change to progress state selected cases?  Only approved cases will be changed to progress state.',
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#DD6B55",
                confirmButtonText: "CONFIRM",
                cancelButtonText: "CANCEL",
                closeOnConfirm: false,
                closeOnCancel: false
                },function(inputValue){
                    
                if (inputValue===false)
                {
                    var $form_parent = $("table");
                    $form_parent.find('[name^="sel_ids"]').prop('checked', false);
                    swal.close();
                } 
                else 
                {/*confirm*/
                    swal.close();                        
                    var $form = $('#multi_progress_form');
                    $.each( $('.dataTable [name^="sel_ids"]:checked'), function() {
                        var $input = $('<input type="hidden" name="' + this.name + '" value="' + $(this).val() + '" checked />');
                        
                        $form.append($input);
                    });
            
                    $.ajax({
                        url: form.action,
                        type: form.method,
                        data: $(form).serialize(),
                        dataType: "json",
                        success: function(data) {
                            console.log(data);
                            if(data.status == true)
                            {
                                
                                swal({
                                    title: "Success", 
                                    text: data.success, 
                                    type: "success"
                                    },
                                    function(){ 
                                        oTable.ajax.reload();
                                    }
                                );
                            }
                            else
                            {
                                swal({
                                title: "Warning", 
                                text: data.warning, 
                                type: "warning"
                                });
                            }
                        }
                    });
                }
            });
        } 
        else 
        {
            swal({
                title: "Warning", 
                text: 'Please select atleast one checkbox', 
                type: "warning"
            });
        }
    }
});
function initFetchDataLoader() {
    $('.app-data-loader').html(`<div class="loader-19"></div>`);
}

function removeFetchDataLoader(attr) {
    $('[data-module=' + attr + ']').empty().removeClass('app-data-loader data-loader-block data-loader-30');
}

function PostData(url, data = "", method = 'POST') {

    return new Promise((resolve, reject) => {
        $.ajax({
            url: url,
            type: method,
            data: data,
            success: function(data) {
                resolve(data)
            },
            error: function(error) {
                reject(error)
            },
        })
    })
}


function initLoader(attr) {

    $(attr).html(loaderIcon);
}

function amountFormat(amount) {

    //return Number(amount).toFixed(2).toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}

function initMenuActive() {

    let pathName = location.pathname;
    let route = pathName.split('/');
    let url = "";
    let origin = location.origin;
    var filtered = route.filter(function(el) {
        return el !== "";
    });
    url = origin + '/' + filtered[0];
    let menu = $('.nav-item a[href^="' + url + '"]');
    let parentId = menu.parent().parent().parent().data('id');
    $('#app-menu-' + parentId).addClass('menu-open');
    $('#app-nav-menu-' + parentId).addClass('active');
    menu.addClass('active')
}

function intiNotification(message, type) {

    let title = "";
    let positionClass = "toast-top-right";
    let containerId = "toast-top-right";
    let timeOut = "5000";

    switch (type) {
        case 'success':
            toastr.success(message, title, {
                timeOut: timeOut,
            })
            break;
        case 'warning':
            toastr.warning(message, title, {
                timeOut: timeOut,
            })
            break;
        case 'error':
            toastr.error(message, title, {
                timeOut: timeOut,
            })
            break;

        default:
            break;
    }
}

function limitText(str, limit) {
    if (str.length > limit) {
        return str.substring(0, limit) + '...';
    } else {
        return str;
    }
}

(function($) {
    $.fn.inputFilter = function(inputFilter) {
        return this.on("input keydown keyup mousedown mouseup select contextmenu drop", function() {
            if (inputFilter(this.value)) {
                this.oldValue = this.value;
                this.oldSelectionStart = this.selectionStart;
                this.oldSelectionEnd = this.selectionEnd;
            } else if (this.hasOwnProperty("oldValue")) {
                this.value = this.oldValue;
                this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
            } else {
                this.value = "";
            }
        });
    };
}(jQuery));

function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      
      reader.onload = function(e) {
        $('#'+$(input).data('id')).attr('src', e.target.result);
      }
      
      reader.readAsDataURL(input.files[0]); // convert to base64 string
    }
  }

  
function resetDataTable(e, t) {
    "datatable" == t && $(e).DataTable().draw()
}
