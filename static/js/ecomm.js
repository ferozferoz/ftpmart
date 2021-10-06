var profileInfo;

$(document).ready(function(){
  $(".nav-tabs a").click(function(){
    $(this).tab('show');
  });
});

function cancelEditForm(){
    document.getElementById("home").innerHTML = profileInfo;
}


