$(function(){

function openSB() {
  $("#sidebar").addClass("active");
  $("#overlay").addClass("active");
  $("body").addClass("sb-open");
}

function closeSB() {
  $("#sidebar").removeClass("active");
  $("#overlay").removeClass("active");
  $("body").removeClass("sb-open");
}

  $("#menuToggle").on("click", function(){
    $("#sidebar").hasClass("active") ? closeSB() : openSB();
  });

  $("#overlay").on("click", closeSB);

  $(".sb-body li a").on("click", function(){
    $(".sb-body li").removeClass("sb-on");
    $(this).closest("li").addClass("sb-on");
    closeSB();
  });

  $(window).on("resize", function(){
    if(window.innerWidth >= 992) closeSB();
  });

});