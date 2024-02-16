let tbody = document.querySelectorAll('tbody > tr');
let thead = document.querySelectorAll('thead > tr');

let iCell_count;
let iCell_need_count;

thead.forEach(element=> {
    let childrenThead = element.children;
    for(let i =0;i<childrenThead.length; i++)
    {
        if(childrenThead[i].innerText == 'Нужно')
            iCell_need_count = i;
        else if (childrenThead[i].innerText == 'Кол-во на складе')
            iCell_count = i;

        if (iCell_count != null && iCell_need_count != null)
            break
    }
});

tbody.forEach(element=>{
    let color;

    cell_count = element.children[iCell_count].innerText
    cell_need_count = element.children[iCell_need_count].innerText
    
    if (cell_count > cell_need_count)
        color = 'rgba(70, 172, 78, 0.658)';
    else
        color = 'rgba(243, 74, 74, 0.767)';

    element.style.backgroundColor = color;
})

let button = document.getElementById("upload_pbc");
let popup_container = document.querySelector(".popup-container")
let button_close_popup = document.querySelector(".exit_popup")
let formComponents = document.querySelector(".upload_file_form_main")
let formGerbers = document.getElementById('gerber_form')
let input_form = document.querySelectorAll(".upload_file_form_main > p > input")
let li = document.querySelectorAll('.files > ul > li')
let p = document.querySelectorAll('.upload_file_form_main > p')

for(let i = 0; i < p.length; i++)
{
    if(p[i].children.length > 3)
    {
        li[i].classList.remove('not-exist')
        li[i].classList.add('exist')
    }
}

formComponents.addEventListener("submit", (e)=>{
    e.preventDefault();
    let isEmpty = true

    for(let i = 0;i < input_form.length; i++)
    {
        try
        {
            if(input_form[i].files.length !== 0)
            {
                isEmpty = false
                break;
            }
        }
        catch
        {
            if(input_form[i].checked)
            {
                isEmpty = false
                break;
            }
        }
    }

    if(!isEmpty)
        sendComponentsRequest(formComponents)
})

button_close_popup.addEventListener("click",()=>{
    popup_container.classList.add("hide");
    document.body.style.overflow = 'hidden !important';
})

button.addEventListener("click", ()=>{
    popup_container.classList.remove("hide");
    document.body.style.overflow = 'auto';
});

formGerbers.addEventListener("submit", (e)=>{
    e.preventDefault()
    sendComponentsRequest(formGerbers)

})

function sendComponentsRequest(form)
{
    let formData = new FormData(form)
    let xhr = new XMLHttpRequest();
    
    xhr.open(form.getAttribute('method'), form.getAttribute('action'));
    
    xhr.send(formData);

    xhr.onload  = ()=>{
        if(xhr.status == 200)
            location.reload();
        else
            alert('Ошибка при отправке запроса' + xhr.responseText)
    }
}