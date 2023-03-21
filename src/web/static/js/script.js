function loader() {
    document.getElementById("loader").style.display = "flex";
  }

function validatePdf(fileElement) {
  var fileName = fileElement.value;
  var fileType = fileName.substr(fileName.lastIndexOf("."), fileName.length).toLowerCase();
  if (fileType != ".pdf") {
    alert("This is not pdf file!");
    fileElement.value = "";
  }
}