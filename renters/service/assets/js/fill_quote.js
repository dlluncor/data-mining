var ctrl = {};

ctrl.getRenterForm = function() {
  var d = {
    "insurance_type": "renters",
    "purchase_category": $('#form-purchase-category').val(),
    "dob": $('#form-dob').val(),
    "first_name": $('#form-first-name').val(),
    "last_name": $('#form-last-name').val(),
    "address": $('#form-address').val(),
    "city": $('#form-city').val(),
    "state": $('#form-state').val(),
    "zip_code": $('#form-zip-code').val(),
    "phone_number": $('#form-phone-number').val(),
    "email_address": $('#form-email-address').val()
  };
  var form = {
    "renter_form": d
  };
  return form;
}

ctrl.encrypt = function(text) {
  var pem = "-----BEGIN PUBLIC KEY-----" +
            "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwb7gVFbFCHd3vrPMUlBs" +
            "4WzNDc14Lw73KGjhxWix6K9TDJWtVBVPkyD5aEku1EN+tEKW8OwLMZSW6O5q3XBE" +
            "ycItJEWS2gBJ2GYsvXIWkVMgELz2oUm/obOjoTGbKE/51n9q1xXtNpZ2gCug2JH6" +
            "0lH0KmNToFpjSJ8yzcUuC5XfbMQLryRlE0soeucMMYJ7Yrwq5Up+EXVh24rgs9Ak" +
            "/iNzcFVJtOHLXxXheR4TftPZP6kyz7NowY3YHPBBOiXe0nQKbNhWUXR1vmNNLzvz" +
            "jE3F9Cmv8I+iNTpNbHrqcUbXkx/bDfcIsWqaVVdZBeq2mEP1BrXTsIHQAu6IAhFj" +
            "3wIDAQAB" +
            "-----END PUBLIC KEY-----";
  var publicKey = forge.pki.publicKeyFromPem(pem);
  var encrypted = publicKey.encrypt(text, 'RSA-OAEP');
  var msg = forge.util.encode64(encrypted);
  return msg;
};

ctrl.getPaymentForm = function() {
  // Need to encrypt this on client side.
  var d = {
    "card_number": $('#pform-cardnumber').val(),
    "cvc": $('#pform-cvc').val(),
    "exp_month": $('#pform-exp-month').val(),
    "exp_year": $('#pform-exp-year').val(),
    "billing_address": $('#pform-billing-address').val(),
  };
  // Encrypt the whole payment form.
  var encrypted_d = ctrl.encrypt(JSON.stringify(d));
  var encrypted = {
    "encrypted_payment_form" : encrypted_d 
  };
  return encrypted;
};

// showEstimate gets the price of the estimated rental policy.
ctrl.showEstimate = function() {
  window.console.log('ctrl.showEsitmate');
  var form = ctrl.getRenterForm();
  $.ajax({
    url: "/price",
    context: document.body,
    data: JSON.stringify(form),
    contentType : 'application/json',
    type: "POST"
  }).done(function(data) {
     window.console.log(data);
     var price = parseFloat(data);
     var roundedPrice = Math.round(price * 100) / 100;
     $('#estimated-value').text('$' + roundedPrice);
     // Save price to local storage.
     localStorage['estimated-value'] = roundedPrice;
     //$( this ).addClass( "done" );
  })
    .fail(function() {
     alert( "error" );
  })
  ;
}

// pay actually pays for the cost of the insurance.
ctrl.pay = function() {
  window.console.log('ctrl.pay');
  var form = ctrl.getRenterForm();
  var payment = ctrl.getPaymentForm();
  form['payment_form'] = payment;
  // Gather all the form values into a dictionary to send to the backend.
  $.ajax({
    url: "/buy",
    context: document.body,
    data: JSON.stringify(form),
    contentType : 'application/json',
    type: "POST"
  }).done(function(data) {
     window.console.log(data);
     window.location = '/payment_complete';
  })
    .fail(function() {
     alert( "error" );
  })
  ;
}