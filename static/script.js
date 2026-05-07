document.querySelectorAll('input[type ="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        let form = this.closest('form')
        form.submit()
    })
})


document.querySelectorAll('.menu-btn').forEach(btn =>{
    btn.addEventListener('click', function() {
        this.nextElementSibling.classList.toggle('active')
    })
})

document.querySelectorAll('.update-btn').forEach(btn =>{
    btn.addEventListener('click', function() {
        let input = this.previousElementSibling
        let confirm = this.nextElementSibling
        let deleteForm = this.closest('li').querySelector('form[action$="/delete"]')


        input.style.display = 'block'
        confirm.style.display = 'block'
        this.style.display = 'none'
        if(deleteForm)deleteForm.style.display = 'none' 
 
    })
})

document.querySelectorAll('.add-btn').forEach(btn =>{
    btn.addEventListener('click', function() {
        let input = this.nextElementSibling
        let submit = input.nextElementSibling
        input.style.display = 'block'
        submit.style.display = 'block'
        this.style.display = 'none'
        input.focus()
    })
})

document.querySelectorAll('.add-input').forEach(input=>{
    input.addEventListener('click', function(e) {
        e.stopPropagation()
    })
})

let toggleBtn = document.getElementById('toggle')
if(toggleBtn) {
    toggleBtn.addEventListener('click', function() {
        let input = document.getElementById('password')
        if(input.type === 'password') {
            input.type = 'text'
            this.textContent = 'hide password'
        } else {
            input.type = 'password'
            this.textContent = 'show password'
        }
    })
}

let usernameInput = document.querySelector('input[name="username"]')
if(usernameInput) {
    usernameInput.addEventListener('keydown', function(e) {
        if(e.key === 'Enter') {
            e.preventDefault()
            document.querySelector('input[name="password"]').focus()
        }
    })
}