$(document).ready(function() {

    function rect2(canvas, c) {
          var ctx = canvas.getContext("2d");
          ctx.fillStyle = c[0];
          ctx.fillRect(0, 0, canvas.width/2, canvas.height);
          ctx.fillStyle = c[1];
          ctx.fillRect(canvas.width/2, 0, canvas.width/2, canvas.height);
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

  $( "canvas[data-type='yocolormaker']" ).each(function( index ) {
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
});