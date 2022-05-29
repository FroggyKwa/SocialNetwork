const phone_field = ($("#id_phone")[0]);
const error = $(".error")[0];
const email_field = $("#id_email")[0];

function phonenumber(inputtxt) {
  var reg = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im;
  var digits = inputtxt.replace(/\D/g, "");
  return reg.test(digits);
}



$(document).ready(function() {
  $(phone_field).on("input", function () {
    var check = phonenumber(phone_field.value);
    console.log(check)
    if (!check)
    {
      phone_field.setCustomValidity("Phone format is wrong!");
      phone_field.reportValidity();
    }
    else {
      phone_field.setCustomValidity("");
    }
  });

  $(email_field).on("input", function()
  {
    console.log("1231");
    if (email_field.validity.tooShort)
    {
      email_field.setCustomValidity("Provided email is too short!")
    }
    if (email_field.validity.typeMismatch)
    {
      email_field.setCustomValidity("Entered value needs to be an e-mail address.")
    }
    else
    {
      email_field.setCustomValidity("");
    }
  });
});
