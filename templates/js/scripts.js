$(document).ready(function(){
fields_taken = []
    $.ajax({
      url: "/fetchlabels",
      type: "get",
      data: {},
      success: function(response) {
        data = response.label_data
        $.each(data, function(key, value) {
            dropdown = '<select id="'+key+'" name="'+key+'">'
             $.each(value, function(i, o) {
                    dropdown+=' <option value="'+o+'">'+o+'</option>';
             });
            dropdown+=' </select>'

            row = '<tr > <td>'+ key +'</td> <td> '+ dropdown +'</td> </tr>'

            $('#filters tr:last').after(row);
            fields_taken.push(key);
        });
        loadOthers()
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
});


function loadOthers(){
 $.ajax({
      url: "/fetchfeatures",
      type: "get",
      data: {},
      success: function(response) {
        data = response.features
        $.each(data, function(key, value) {
            if(!fields_taken.includes(value)){
                 select = ""
            if(value=='Time' || value == 'time'){
                select = '<input type="time" id="'+value+'" name="'+value+'" value="23:59" required> </input>'
            }else{
                select = '<input type="number" id="'+value+'" name="'+value+'" value="1" required> </input>'
            }

            row = '<tr > <td>'+ value +'</td> <td> '+ select +'</td> </tr>'

            $('#filters tr:last').after(row);
            }
        });
         row = '<tr > <td>&nbsp</td> <td> <input type="button" value="predict" onClick="predict()"></input></td> </tr>';
         $('#filters tr:last').after(row);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
}



function predict(){
    var $inputs = $('#filters :input');

    var values = {};
    $inputs.each(function() {
        if(this.name!=""){
            if(!isNaN($(this).val())){
                values[this.name] = parseInt($(this).val());
            }else{
                values[this.name] = $(this).val();
            }
        }

    });

    $.ajax({
      url: "/predict",
      type: "post",
      data: values,
      success: function(response) {
        alert(response)
      },
      error: function(xhr) {
        //Do Something to handle error
      }
     });
}


