$(document).ready(function(){
    $('select').change(function(){
        if($('select option:selected').text() == "TRACKS"){
        $('label').show();
        }
        else{
        $('label').hide();
        }
    })
});