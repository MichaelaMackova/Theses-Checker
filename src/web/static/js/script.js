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

function toggleIcon(sectionId){
  $('#'+sectionId+' .section-title i').toggleClass('fa-chevron-up fa-chevron-down');
}

function toggleSection(sectionId){
  $('#'+sectionId+' .section-content').slideToggle();
  toggleIcon(sectionId);
}
