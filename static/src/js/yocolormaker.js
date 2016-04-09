$(document).ready(function() {

  $('.product-info').each(function (event) {
    var product_info = this;

    /* enable product lang selected only */
    $( product_info ).on('change', "select[name='language_select']",
      function () {
        var $all_product_lines = $("ul[class='ul-product-detail-add-to-cart']", product_info);
        $all_product_lines.attr("style","display:none;");

        var $select = $("select[name='language_select']");

        $("li[class='li-product-detail']", product_info).each(function () {
          data_lang = $( this ).attr("data-lang");
          if (data_lang === $select.val() ) {
            $( this ).parent().attr("style","display:block;");
          }
        });
        }
      )
      $( product_info ).find("select[name='language_select']").change();
    }
  )

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

    function bgimg(tag, img) {
      backgroundvalue  = "url("+img+")";
      /*backgroundvalue  = "url(http://babache-erp-st.yotech.ch/website/image/product.template/4420_69929a6/image/26x26)";*/
      $(tag).css("background-image", backgroundvalue);
      $(tag).css("background-repeat", "no-repeat");
      $(tag).css("background-size", "cover");
    }


  $( "label[data-type='yocolormaker']" ).each(function( index ) {
    if ($(this).attr("data-params")) {
      $(this).attr("data-params");
      data   = JSON.parse($(this).attr("data-params"));
      drawfunc = data[0];
      params = data.slice(1,data.length);
    }
    else {
      drawfunc = "rect1";
    }
    switch (drawfunc) {
      case "rect1": break;
      case "rect2": rect2(this, params ); break;
      case "rect3": rect3(this, params ); break;
      case "rect4": rect4(this, params ); break;
      case "bgimg": bgimg(this, $(this).attr("data-bgimg") ); break;
    }
  });

  /* find default value and select it */
  /* $(".ul-product-detail-add-to-cart").find("input[checked=checked]").parent().parent().parent().addClass("selected"); */
  lang = $("select[name='language_select']").val();
  if (lang) {
    selector=".li-product-detail[data-lang="+lang+"]";
  }
  else {
    selector=".li-product-detail";
  }
  $(selector).first().parent().addClass("selected");

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
