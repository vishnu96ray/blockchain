$("#userregister").click(function(){
                $('#signup-form').validate({ // initialize the plugin
                    rules: {
                        pan: {
                            required: true
                        },
                        joining_amt: {
                            required: true
                        },
                        email: {
                            required: true,
                            email: true
                        },
                        username: {
                            required: true,
                            alphanumericonly: true
                        },
                        mobile: {
                            required: true,
                            digits: true,
                            minlength : 4,
                            maxlength : 14
                        },
                        password: {
                            required: true,
                            minlength : 5
                        }
                    },
                    submitHandler: function (form) {
                    $('#userregister').attr('disabled', 'disabled').html('Please Wait ...');
                        $.ajax({
                           type: "POST",
                           url: "/accounts/register/user/",
                           data: $("#signup-form").serialize(), // serializes the form's elements.
                           success: function(data)
                           {
                               if (data == 1)
                               {
                                   $('.alert-success').removeClass('hidden');
                                   $('.alert-info').addClass('hidden');                                   
                                   $('.form-control').val("");
				   setTimeout(function(){
			              document.location="/business/";
					}, 5000);
                               }
                               if (data == 2)
                               {
                                   $('.alert-info').removeClass('hidden');
                                   $('.alert-success').addClass('hidden');

                               }
                               $('#userregister').removeAttr('disabled').html('Submit');

                           }
                         });
                    }
                });



            });