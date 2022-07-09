function togglebutton(elementId) {
  var button = document.getElementById(elementId);
  var x = button.getElementsByTagName("img");
  var state = button.dataset.state == "true";
  button.dataset.state = (!state).toString();
  x[0].classList.toggle("hidden-image");
  x[1].classList.toggle("hidden-image");

  filterElements = document.getElementsByClassName("hyperlink-filter");
  state_of_filter = false;
  for (var i = 0; i < filterElements.length; i++) {
    state_of_filter =
      state_of_filter | (filterElements.item(i).dataset.state == "true");
  }
  if (state_of_filter) {
    document.getElementById("orderSelect").setAttribute("disabled", "disabled");
  } else {
    document.getElementById("orderSelect").removeAttribute("disabled");
  }
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
