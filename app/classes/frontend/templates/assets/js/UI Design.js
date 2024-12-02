
// JS for Admin SideNav
const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});

// JS for matching passwords
function CompareFields(f1, f2, caseinsensitive)
{
   var val1 = document.getElementById(f1).value;
   var val2 = document.getElementById(f2).value;
   if( caseinsensitive )
   {
      val1 = val1.toUpperCase();
      val2 = val2.toUpperCase();
   }
   val1 = val1.replace(/^\s*/,"");
   val1 = val1.replace(/\s*$/,"");
   if( val1.length == 0 ) { return; }
   val2 = val2.replace(/^\s*/,"");
   val2 = val2.replace(/\s*$/,"");
   if( val2.length == 0 ) { return; }
   if( val1 == val2 ) { return; }
   // An alert box is used for verification failures.
   // The message may be changed as appropriate for your installation.
   // Or, replace alert(...) with your preferred error message system.
   alert("The passwords need to be identical.");
}


// Sign-up button 
$(':text').keyup(function() {
  if($('password1').val() != "" && $('password2').val() != "") {
     $('Sign-up').removeAttr('disabled');
  } else {
     $('Sign-up').attr('disabled', true);   
  }
});


