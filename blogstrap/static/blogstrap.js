var converter = new showdown.Converter({
  tables: true,
  strikethrough: true,
  simplifiedAutoLink: true,
});

window.onload = function () {

  var blogpost = document.getElementsByClassName("blogstrap");
  //TODO: ES6 only. Provide support for older browsers
  for (div of blogpost) {
    text = div.textContent.trim().split('/\n */').join('\n');
    var html = converter.makeHtml(text);
    div.innerHTML = html;
  }

  // Add .table to our generated tables
  tables = blogpost[0].getElementsByTagName("table");
  for (table of tables) {
    table.classList.add("table");
  }

  document.body.style.visibility = "visible";
};
