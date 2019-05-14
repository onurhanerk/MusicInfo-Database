$(document).ready(function(){
    $('select').change(function(){
        if($('select option:selected').text() == "TRACKS"){
        $('labelTrack').show();
        }
        else{
        $('labelTrack').hide();
        }
    })
});
$(document).ready(function(){
    $('select').change(function(){
        if($('select option:selected').text() == "ALBUMS"){
        $('labelAlbum').show();
        }
        else{
        $('labelAlbum').hide();
        }
    })
});
$(document).ready(function(){
    $('select').change(function(){
        if($('select option:selected').text() == "ARTIST"){
        $('labelArtist').show();
        }
        else{
        $('labelArtist').hide();
        }
    })
});
$(document).ready(function(){
    $('select').change(function(){
        if($('select option:selected').text() == "GENRES"){
        $('labelGenres').show();
        }
        else{
        $('labelGenres').hide();
        }
    })
});
