const add_button = document.getElementById("add_plan_button");
const add_meal_wrapper = document.getElementById("add-meal-wrapper");

const meal_plan_form = `
    <div class="row">
        <div class="col-8 my-3">
            <label class="form-label fs-5 fw-bold">Plan Name</label>
            <input type="text" class="form-control" name="plan_name" required>
        </div>
        <div class="col-4 my-3">
            <label class="form-label fs-5 fw-bold">Price</label>
            <input type="text" name="plan_price" class="form-control" placeholder="I.e 150$" required>
        </div>
        <div class="col-12 my-3">
            <label class="form-label fs-5 fw-bold">Plan Description</label>
            <textarea class="form-control" rows="5" placeholder="Plan Description...." name="plan_description" required></textarea>
        </div>
    </div>
`

add_button.addEventListener("click", () => {
    add_meal_wrapper.insertAdjacentHTML("beforeend", meal_plan_form)
})