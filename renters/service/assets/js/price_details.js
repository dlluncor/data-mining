
var rts = {};

rts.priceTemplateStr = '   <div class="plan"> ' +
                     '       <br> ' +
                     '       <div class="title"><%=title%></div> ' +
                     '       <div class="price" id="<%=price_div_id%>">$178/year</div> ' +
                     '       <div class="description"> ' +
                     '           <b><%=personal_liability%></b> Personal Liability ' +
                     '           <br> ' +
                     '           <b><%=personal_property%></b> Personal Property ' +
                     '           <br> ' +
                     '           <b><%=loss_of_use%></b> Loss of Use' +
                     '           <br>' +
                     '          <b><%=deductible%></b> Deductible' +
                     '       </div>' +
                     '       <a class="btn btn-primary" href="#contact-details" onclick="ctrl.showFinalEstimate(\'<%=key%>\'); showNext(\'#contact-details\');mixpanel.track(\'click QUOTE:#<%=price_div_id%>:Select\');window.purchase_category=\'<%= key %>\'">Select</a>' +
                     '   </div>';

rts.priceTemplate = _.template(rts.priceTemplateStr);

rts.d = {
    "cheap": {
      "key": "cheap",
      "title": "Starter",
      "personal_liability": "$100,000",
      "personal_property": "$4,000",
      "loss_of_use": "$1,000",
      "deductible": "$500",
      "price_div_id": "starter-price",
    },
    "medium": {
      "key": "medium",
      "title": "Split w/ Roommates",
      "personal_liability": "$100,000",
      "personal_property": "$30,000",
      "loss_of_use": "$6,000",
      "deductible": "$1000",
      "price_div_id": "medium-price",
    },
    "deluxe": {
      "key": "deluxe",
      "title": "Deluxe",
      "personal_liability": "$300,000",
      "personal_property": "$60,000",
      "loss_of_use": "$12,000",
      "deductible": "$1000",
      "price_div_id": "deluxe-price",
    }
};

rts.priceCardHtml = function(option) {
  var dataVal = rts.d[option];
  return rts.priceTemplate(dataVal);
};

rts.divId = function(option) {
  var dataVal = rts.d[option];
  return dataVal['price_div_id'];
};
