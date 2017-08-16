function get_search_results(page) {
    var $pager = $('.pager');
    
    $.ajax({
        type  : "GET",
        async : false,
        url   : '/messages/recherche/',
        data  :{
         recherche: $("#recherche").val(),
         to: $("#to").val(),
         page : page,
       },
        cache : false,
        success: function(html) {
             
           $( "#modal-body" ).html( html.produits );
           $('.modals').html(html.modals);
           $pager.attr('data-current-page', page);
           $(".page").val(page);

           // console.log(page)

            /*  if (html === "") {
                  $("#loader_message").html('<p>There were no results that match your search criteria</p>').show();
              } else {
                  $("#loader_message").html('Searching... Please wait <img src="http://www.example.com/monstroid/wp-content/uploads/2016/02/LoaderIcon.gif" alt="Loading">').show();
              }  
              window.busy = false; */
        }
      });

/*$(".recherche").keyup(function (){
    setTimeout(get_search_results, 200);
});*/

}

$(function(){

$("#recherche").on('keyup', function (){
    setTimeout(get_search_results, 200);
}); 
var $pager = $('.pager')

$('#next').on('click', function () {
   var $pager = $('.pager')
    var page = parseInt($pager.attr('data-current-page'));
    console.log(page)
     
    get_search_results(page+1);
}); 
$('#prev').on('click', function () {
   var $pager = $('.pager')
    var page = parseInt($pager.attr('data-current-page'));
    console.log(page)
    

    get_search_results(page-1);
});  




}) 
