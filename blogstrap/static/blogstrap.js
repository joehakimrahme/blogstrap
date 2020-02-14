var converter = new showdown.Converter();

window.onload = function () {
  var blogpost = document.getElementsByClassName("blogstrap");
  //TODO: ES6 only. Provide support for older browsers
  for (div of blogpost) {
    text = div.textContent.trim().split('/\n */').join('\n');
    var html = converter.makeHtml(text);
    div.innerHTML = html;
  }

  document.body.style.visibility = "visible";
};
