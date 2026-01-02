let inputBox=document.querySelector(".input-box");
let addBtn=document.querySelector(".Add-task");
let items=document.querySelector(".new-todo ul")
let completedItem=document.querySelector(".completed-todo ul")

function addItem(text){
   const addItemLi= document.createElement("li")
   const addItemCheckBox=document.createElement("input")
   const addItemSpan=document.createElement("span")
   addItemCheckBox.type="checkBox"
   addItemSpan.innerHTML=text;
   addItemLi.appendChild(addItemCheckBox)
   addItemLi.appendChild(addItemSpan)
   return addItemLi
}

function addTask(event){
    event.preventDefault()
    if(inputBox.value!==""){
    let addedLI=addItem(inputBox.value);
    items.appendChild(addedLI)
    addedLI.querySelector("input").onchange=completeTask
    inputBox.value=""  
    } 
}

function completeTask(){
  let conpletedLi=this.parentNode
  conpletedLi.remove()
  completedItem.appendChild(conpletedLi)
  conpletedLi.querySelector("input").remove()
  let deleteBtn=document.createElement("button")
  deleteBtn.innerText="delete"
  deleteBtn.onclick=deleteTask
  conpletedLi.appendChild(deleteBtn)
}
function deleteTask(){
    this.parentNode.remove()
}
addBtn.addEventListener("click",addTask)