const image_preview_div = document.getElementById("image-preview");
const image_input = document.getElementById("image-input");

let uploaded_images = [];

function display_images() {
    let images = "";
    uploaded_images.forEach((image, index) => {
        images += `
            <div class="col-6 col-md-3 border">
                <img src="${URL.createObjectURL(image)}" class="w-100">
            </div>
        `
    })

    image_preview_div.innerHTML = images;
}

image_input.addEventListener("change", () => {
    for (let i = 0; i < image_input.files.length; i++) {
        uploaded_images.push(image_input.files[i]);
    }
    display_images();
})