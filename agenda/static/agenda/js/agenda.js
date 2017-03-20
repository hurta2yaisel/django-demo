$(document).ready(function () {
    // List contacts
    $('#grid_contacts').click(function (event) {
        event.preventDefault();
        var contact = $('#contacts .item');
        contact.removeClass('list-group-item');
        contact.removeClass('padding-side');
        contact.addClass('grid-group-item');
    });
    /*$("#myform").validate({
     submitHandler: function (form) {
     form.submit();
     }
     });*/
    $('#list_contacts').click(function (event) {
        event.preventDefault();
        $('#contacts .item').addClass('list-group-item');
        $('#contacts .item').addClass('padding-side');
    });


    $(document.body).on('click', '.changeType', function () {
        $(this).closest('.phone-input').find('.type-text').text($(this).text());
        $(this).closest('.phone-input').find('.type-input').val($(this).data('type-value'));
    });

    $(document.body).on('click', '.btn-remove-phone', function () {
        $(this).closest('.phone-input').remove();
    });

    $('.btn-add-phone').click(function () {

        var index = $('.phone-input').length + 1;
        $('.phone-list').append('' +
            '<div class="input-group phone-input">' +
            '<span class="input-group-addon"><i class="glyphicon glyphicon-earphone"></i></span>' +
            '<input type="text" name="phone_number_' + index + '" class="form-control" placeholder="+53 55555555" />' +
            '<input type="hidden" name="phone_type_' + index + '" class="type-input" value="" />' +
            '<span class="input-group-btn">' +
            '<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><span class="type-text">Type</span> <span class="caret"></span></button>' +
            '<ul class="dropdown-menu" role="menu">' +
            '<li><a class="changeType" href="javascript:;" data-type-value="mobile">Mobile</a></li>' +
            '<li><a class="changeType" href="javascript:;" data-type-value="home">Home</a></li>' +
            '<li><a class="changeType" href="javascript:;" data-type-value="work">Work</a></li>' +
            '<li><a class="changeType" href="javascript:;" data-type-value="fax">Fax</a></li>' +
            '<li><a class="changeType" href="javascript:;" data-type-value="other">Other</a></li>' +
            '</ul>' +
            '<button class="btn btn-default btn-remove-phone" type="button"><span class="glyphicon glyphicon-remove"></span></button>' +
            '</span>' +
            '</div>'
        );

    });
    $('#btn_avatar_thumbnail').click(function (arg) {
        var container = $('#container_avatar_thumbnail');
        container.append('' +
            '<div class="input-group phone-input">' +
            '<span class="input-group-addon"><i class="glyphicon glyphicon-picture"></i></span>' +
            '<input type="file" name="avatar" class="form-control image-uploader" value=""/>' +
            '</div>'
        );
        $('#div_avatar_thumbnail').remove();
    });
    $('#confirm-delete').on('show.bs.modal', function (e) {
        $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
    });
    // Delete contact

    // New and Edit Contact
    $('#contact_form').bootstrapValidator({
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            first_name: {
                validators: {
                    stringLength: {
                        min: 2
                    },
                    notEmpty: {
                        message: 'Please supply your first name'
                    }
                }
            },
            last_name: {
                validators: {
                    stringLength: {
                        min: 2
                    },
                    notEmpty: {
                        message: 'Please supply your last name'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your email address'
                    },
                    emailAddress: {
                        message: 'Please supply a valid email address'
                    }
                }
            },
            phone: {
                validators: {
                    notEmpty: {
                        message: 'Please supply your phone number'
                    },
                    phone: {
                        country: 'CU',
                        message: 'Please supply a valid phone number with area code'
                    }
                }
            },
            address: {
                validators: {
                    stringLength: {
                        min: 8
                    },
                    notEmpty: {
                        message: 'Please supply your address'
                    }
                }
            }
        }
    }).on('success.form.bv', function (e) {
        $('#success_message').slideDown({opacity: "show"}, "slow"); // Do something ...
        $('#contact_form').data('bootstrapValidator').resetForm();

        // Prevent form submission
        e.preventDefault();

        // Get the form instance
        var $form = $(e.target);

        // Get the BootstrapValidator instance
        var bv = $form.data('bootstrapValidator');

        // Use Ajax to submit form data
        $.post($form.attr('action'), $form.serialize(), function (result) {
            console.log(result);
        }, 'json');
    });
});
/* """url(r'^$', HomePageView.as_view(), name='home', ),
 url(r'^$', HomePageView.as_view(), name='contact_list', ),
 url(r'^contact/new/$', CreateContact.as_view(), name='contact_new'),
 url(r'^contact/edit/(?P<pk>\d+)$', HomePageView.as_view(), name='contact_edit'),
 url(r'^contact/delete/(?P<pk>\d+)$', HomePageView.as_view(), name='contact_delete'),"""*/
