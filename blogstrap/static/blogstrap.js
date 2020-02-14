var converter = new showdown.Converter();
var blogpost = document.getElementsByClassName("blogstrap");

for (div of blogpost) {
  text = div.textContent.trim().split('/\n */').join('\n');
  var html = converter.makeHtml(text);
  div.innerHTML = html;
}

document.body.style.visibility = "visible";
