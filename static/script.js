document.getElementById("upload-form").addEventListener("submit", function (e) {
  e.preventDefault();

  let fileInput = document.getElementById("file-input");
  let formData = new FormData();
  formData.append("file", fileInput.files[0]);

  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("result").innerText = data.result;
      document.getElementById("preview-image").src = URL.createObjectURL(
        fileInput.files[0]
      );
      document.getElementById("preview-image").style.display = "block";
    })
    .catch((error) => console.error("Error:", error));
});
