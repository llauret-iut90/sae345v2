function details(id) {
    const url = "http://127.0.0.1:5000/admin/commande/" + id
    location.replace(url);
}

let loadFile = function (event) {
            let reader = new FileReader();
            reader.onload = function () {
                let img_output = document.getElementById('img_output');
                img_output.src = reader.result;
                // print(img_output.src);
            };
            reader.readAsDataURL(event.target.files[0]);
        };
