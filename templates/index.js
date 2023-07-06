// JavaScript logic
function showInputFields() {
  var docType = document.getElementById("doc-type").value;
  var textInput = document.getElementById("text-input");
  var pdfInput = document.getElementById("pdf-input");

  if (docType === "text") {
    textInput.style.display = "block";
    pdfInput.style.display = "none";
  } else if (docType === "pdf") {
    textInput.style.display = "none";
    pdfInput.style.display = "block";
  }
}

function translateDocument() {
  // Add your translation logic here
  var docType = document.getElementById("doc-type").value;
  var text = "";
  var file = null;

  if (docType === "text") {
    text = document.getElementById("text").value;
    console.log("Translating text:", text);
    // Add your translation code for text input
  } else if (docType === "pdf") {
    file = document.getElementById("pdf").files[0];
    console.log("Translating PDF:", file.name);
    // Add your translation code for PDF input
  }

  // Add your translation code here
}
