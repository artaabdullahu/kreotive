 $(document).ready(function() {

     $("#sign-in").popover({
         html: true,
         placement: "bottom",
         content: function () {
             return $("#log-in-form").html();
         }
     });

     $("#share").popover({
         html: true,
         placement: "top",
         content: function () {
             return $("#share-social-media").html();
         }
     });


 });

      function goBack() {
         window.history.back();
     }

$(document).ready(function() {
    $(".dropdown-toggle").dropdown();
});
