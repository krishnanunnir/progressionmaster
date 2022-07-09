function togglebutton(elementId) {
  var button = document.getElementById(elementId);
  var x = button.getElementsByTagName("img");
  x[0].classList.toggle("hide-image");
  x[1].classList.toggle("hide-image");
}

function toggleElement(elementClass) {
  elements = document.getElementsByClassName(elementClass);
  for (var i = 0; i < elements.length; i++) {
    elements.item(i).classList.toggle("hide-" + elementClass);
  }
}
function filterRatingAbove4Amazon(elementId) {
  togglebutton(elementId);
  toggleElement("amazon-rated-above-4");
}

function filterRatingAbove4Goodreads(elementId) {
  togglebutton(elementId);
  toggleElement("goodreads-rated-above-4");
}

function filterKindleUnlimited(elementId) {
  togglebutton(elementId);
  toggleElement("has-kindle-unlimited");
}

function filterAudible(elementId) {
  togglebutton(elementId);
  toggleElement("has-audiobook");
}
