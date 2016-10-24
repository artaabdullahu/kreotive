// $(document).ready(function () {
//
//     $("#filter a").click(function () {
//         var category = $(this).data("category");
//         $(".article").hide();
//         var is_four = 0;
//         var articles = document.getElementsByClassName(category);
//         if (articles.length > 0) {
//             $(articles[0]).parent().addClass("active");
//         }
//         $(".article").each(function (idx) {
//             var item_class = $(this).find("i").attr("class");
//             if( item_class.indexOf(category) >= 0){
//                 if (!($(this).hasClass("active"))){
//                     if (is_four < 2){
//                         $(this).removeClass("col-md-8");
//                         $(this).addClass("col-md-4");
//                         if (is_four == 1){
//                             is_four = 2;
//                         } else {
//                             is_four += 1;
//                         }
//                     } else {
//                         if (is_four >= 2) {
//                             $(this).removeClass("col-md-4");
//                             $(this).addClass("col-md-8");
//                             if (is_four == 3) {
//                                 is_four = 0;
//                             } else {
//                                 is_four += 1
//                             }
//                         }
//                     }
//                 } else {
//                     $(this).removeClass("col-md-4");
//                     $(this).addClass("col-md-8");
//                 }
//                 $(this).show(350);
//             }
//
//         });
//
//         return false;
//     });
// });