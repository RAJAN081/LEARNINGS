// Selectors
const toDoInput = document.querySelector('.todo-input');
const toDoBtn = document.querySelector('.todo-btn');
const toDoList = document.querySelector('.todo-list');
const standardTheme = document.querySelector('.standard-theme');
const lightTheme = document.querySelector('.light-theme');
const darkerTheme = document.querySelector('.darker-theme');

// Event Listeners
toDoBtn.addEventListener('click', addToDo);
toDoList.addEventListener('click', handleTaskClick);
document.addEventListener("DOMContentLoaded", loadTodos);
standardTheme.addEventListener('click', () => changeTheme('standard'));
lightTheme.addEventListener('click', () => changeTheme('light'));
darkerTheme.addEventListener('click', () => changeTheme('darker'));

// Apply saved theme or default theme
let savedTheme = localStorage.getItem('savedTheme') || 'standard';
changeTheme(savedTheme);

// Function to Add Task
function addToDo(event) {
    event.preventDefault();
    if (toDoInput.value.trim() === '') {
        alert("You must write something!");
        return;
    }

    // Create Task Container
    const toDoDiv = document.createElement("div");
    toDoDiv.classList.add('todo', `${savedTheme}-todo`);

    // Check Button (✔) - BEFORE the Task Text
    const checked = document.createElement('button');
    checked.innerHTML = '✔'; 
    checked.classList.add('check-btn', `${savedTheme}-button`);
    toDoDiv.appendChild(checked);

    // Task Text
    const newToDo = document.createElement('li');
    newToDo.innerText = toDoInput.value;
    newToDo.classList.add('todo-item');
    toDoDiv.appendChild(newToDo);

    // Delete Button (❌) - AFTER the Task Text
    const deleted = document.createElement('button');
    deleted.innerHTML = '❌';
    deleted.classList.add('delete-btn', `${savedTheme}-button`);
    toDoDiv.appendChild(deleted);

    // Append to List
    toDoList.appendChild(toDoDiv);

    // Save to Local Storage
    saveToLocal(toDoInput.value);

    // Clear Input Field
    toDoInput.value = '';
}

// Function to Handle Task Click (Complete/Delete)
function handleTaskClick(event) {
    const item = event.target;

    // Delete Task
    if (item.classList.contains('delete-btn')) {
        const todo = item.parentElement;
        todo.classList.add("fall");
        removeLocalTodos(todo);
        todo.addEventListener('transitionend', () => todo.remove());
    }

    // Mark Task as Completed
    if (item.classList.contains('check-btn')) {
        item.parentElement.classList.toggle("completed");
    }
}

// Save Task to Local Storage
function saveToLocal(todo) {
    let todos = localStorage.getItem('todos') ? JSON.parse(localStorage.getItem('todos')) : [];
    todos.push(todo);
    localStorage.setItem('todos', JSON.stringify(todos));
}

// Load Tasks from Local Storage
function loadTodos() {
    let todos = localStorage.getItem('todos') ? JSON.parse(localStorage.getItem('todos')) : [];

    todos.forEach(todo => {
        // Create Task Container
        const toDoDiv = document.createElement("div");
        toDoDiv.classList.add("todo", `${savedTheme}-todo`);

        // Check Button (✔)
        const checked = document.createElement('button');
        checked.innerHTML = '✔';
        checked.classList.add("check-btn", `${savedTheme}-button`);
        toDoDiv.appendChild(checked);

        // Task Text
        const newToDo = document.createElement('li');
        newToDo.innerText = todo;
        newToDo.classList.add('todo-item');
        toDoDiv.appendChild(newToDo);

        // Delete Button (❌)
        const deleted = document.createElement('button');
        deleted.innerHTML = '❌';
        deleted.classList.add("delete-btn", `${savedTheme}-button`);
        toDoDiv.appendChild(deleted);

        // Append to List
        toDoList.appendChild(toDoDiv);
    });
}

// Remove Task from Local Storage
function removeLocalTodos(todo) {
    let todos = localStorage.getItem('todos') ? JSON.parse(localStorage.getItem('todos')) : [];
    const todoText = todo.children[1].innerText; // Get the task text
    todos = todos.filter(t => t !== todoText);
    localStorage.setItem('todos', JSON.stringify(todos));
}

// Change Theme Function
function changeTheme(color) {
    localStorage.setItem('savedTheme', color);
    savedTheme = color;

    document.body.className = color;
    document.getElementById('title')?.classList.toggle('darker-title', color === 'darker');

    document.querySelector('.todo-input').className = `todo-input ${color}-input`;

    // Update Tasks with Theme
    document.querySelectorAll('.todo').forEach(todo => {
        todo.className = todo.classList.contains('completed') 
            ? `todo ${color}-todo completed` 
            : `todo ${color}-todo`;
    });

    // Update Button Colors
    document.querySelectorAll('.check-btn, .delete-btn, .todo-btn').forEach(button => {
        button.className = `${button.classList[0]} ${color}-button`;
    });
}
