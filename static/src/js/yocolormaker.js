$(document).ready(function() {

/*    function rect2(canvas, c) {
          var ctx = canvas.getContext("2d");
          ctx.fillStyle = c[0];
          ctx.fillRect(0, 0, canvas.width/2, canvas.height);
          ctx.fillStyle = c[1];
          ctx.fillRect(canvas.width/2, 0, canvas.width/2, canvas.height);
        } 
    function rect2(canvas, c) {
          div = $("<div class=\"yocolor\" />");
          backgroundvalue  = "linear-gradient(to right, ";
          backgroundvalue += c[0] + " 0%,";
          backgroundvalue += c[0] + " 50%,";
          backgroundvalue += c[1] + " 50%,";
          backgroundvalue += c[1] + " 100%)";
          div.css("background",backgroundvalue);
          div.height( $(canvas).height() );
          div.width( $(canvas).width() );
          div.html( $(canvas).html() );
          $(canvas).replaceWith(div);
    } 

    function rect3(canvas, c) {
          var ctx = canvas.getContext("2d");
          ctx.fillStyle = c[0];
          ctx.fillRect(0, 0, canvas.width/3, canvas.height);
          ctx.fillStyle = c[1];
          ctx.fillRect(canvas.width/3, 0, canvas.width/2, canvas.height);
          ctx.fillStyle = c[2];
          ctx.fillRect(canvas.width*2/3, 0, canvas.width/2, canvas.height);
        } 


    function rect4(canvas, c) {
          var ctx = canvas.getContext("2d");
          ctx.fillStyle = c[0];
          ctx.fillRect(0, 0, canvas.width/2, canvas.height/2);
          ctx.fillStyle = c[1];
          ctx.fillRect(canvas.width/2, 0, canvas.width/2, canvas.height/2);
          ctx.fillStyle = c[2];
          ctx.fillRect(canvas.width/2, canvas.height/2, canvas.width/2, canvas.height/2);
          ctx.fillStyle = c[3];
          ctx.fillRect(0, canvas.height/2, canvas.width/2, canvas.height/2);
        }

*/

    function rect2(tag, c) {
      backgroundvalue  = "linear-gradient(to right, ";
      backgroundvalue += c[0] + " 0%,";
      backgroundvalue += c[0] + " 50%,";
      backgroundvalue += c[1] + " 50%,";
      backgroundvalue += c[1] + " 100%)";
      $(tag).css("background",backgroundvalue);
    }

    function rect3(tag, c) {
      backgroundvalue  = "linear-gradient(to right, ";
      backgroundvalue += c[0] + " 0%,";
      backgroundvalue += c[0] + " 33%,";
      backgroundvalue += c[1] + " 33%,";
      backgroundvalue += c[1] + " 66%,";
      backgroundvalue += c[2] + " 66%,";
      backgroundvalue += c[2] + " 100%)";
      $(tag).css("background",backgroundvalue);
    }

    function rect4(tag, c) {
      backgroundvalue  = "linear-gradient(to right, ";
      backgroundvalue += c[0] + " 0%,";
      backgroundvalue += c[0] + " 25%,";
      backgroundvalue += c[1] + " 25%,";
      backgroundvalue += c[1] + " 50%,";
      backgroundvalue += c[2] + " 50%,";
      backgroundvalue += c[2] + " 75%,";
      backgroundvalue += c[3] + " 75%,";
      backgroundvalue += c[3] + " 100%)";
      $(tag).css("background",backgroundvalue);
    }


  $( "label[data-type='yocolormaker']" ).each(function( index ) {
    $(this).attr("data-params");
    data   = JSON.parse($(this).attr("data-params"));
    drawfunc   = data[0];
    params = data.slice(1,data.length);
    ;
    switch (drawfunc) {
      case "rect2": rect2(this, params ); break;
      case "rect3": rect3(this, params ); break;
      case "rect4": rect4(this, params ); break;    
    }
  });

  /* find default value and select it */
  $(".ul-product-detail-add-to-cart").find("input[checked=checked]").parent().parent().parent().addClass("selected");

  /* when over .ul-product-detail-add-to-cart, select the corresponding variant*/
  $(".ul-product-detail-add-to-cart").hover(  
    function() {
      /* 1. unselect previous variant */
      $(".js_add_cart_variants").find("input[checked=checked]").prop( "checked", false );
      $(".ul-product-detail-add-to-cart.selected").removeClass("selected");

      /* 2. and select new one */
      $( this ).find("input").prop( "checked", true );
      $('input.js_variant_change, select.js_variant_change', this).trigger('change');
      $(this).addClass("selected");
    },
    function() {
      $('input.js_variant_change, select.js_variant_change', this).trigger('change');
    }
  );

});
