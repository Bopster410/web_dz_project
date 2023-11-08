(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})();

function copyTextValue() {
    var value = document.getElementById("tagSelect").value;
    var input_value = document.getElementById("questionTags").value;
    var found_value = input_value.search(value);
    if (found_value == -1) {
        document.getElementById("questionTags").value += value + ' ';
    }
    document.getElementById("tagSelect").value = "Add tag";
}