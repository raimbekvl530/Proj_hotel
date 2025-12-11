// === Инициализация пользователей ===
let users = JSON.parse(localStorage.getItem("users") || "[]");

// Удаляем случайных пользователей с логином "admin"
users = users.filter(u => u.login !== "admin");

// Создаём супер-админа
users.push({login: "admin", pass: "admin", role: "admin"});

// Сохраняем пользователей обратно
localStorage.setItem("users", JSON.stringify(users));

// === Регистрация нового пользователя ===
function register(event) {
    event.preventDefault();
    let login = document.getElementById("regLogin").value;
    let pass = document.getElementById("regPass").value;
    let role = document.getElementById("regRole").value;

    let users = JSON.parse(localStorage.getItem("users") || "[]");

    if (users.find(u => u.login === login)) {
        alert("Такой логин уже существует!");
        return;
    }

    users.push({login, pass, role});
    localStorage.setItem("users", JSON.stringify(users));

    alert("Аккаунт создан!");
    location.href = "login.html";
}

// === Вход пользователя ===
function login(event) {
    event.preventDefault();
    let login = document.getElementById("logLogin").value;
    let pass = document.getElementById("logPass").value;

    let users = JSON.parse(localStorage.getItem("users") || "[]");
    let user = users.find(u => u.login === login && u.pass === pass);

    if (!user) {
        alert("Неверный логин или пароль!");
        return;
    }

    localStorage.setItem("currentUser", JSON.stringify(user));
    location.href = "panel.html";
}

// === Выход пользователя ===
function logout() {
    localStorage.removeItem("currentUser");
    location.href = "login.html";
}

// === Получить роль текущего пользователя ===
function getRole() {
    let user = JSON.parse(localStorage.getItem("currentUser"));
    return user ? user.role : null;
}

// === Получить текущего пользователя ===
function getCurrentUser() {
    return JSON.parse(localStorage.getItem("currentUser"));
}

// === Админ: удалить пользователя ===
function deleteUser(login) {
    let users = JSON.parse(localStorage.getItem("users") || "[]");
    users = users.filter(u => u.login !== login);
    localStorage.setItem("users", JSON.stringify(users));
    renderUsersTable();
}

// === Админ: изменить роль пользователя ===
function changeRole(login, newRole) {
    let users = JSON.parse(localStorage.getItem("users") || "[]");
    users.forEach(u => { if(u.login === login) u.role = newRole; });
    localStorage.setItem("users", JSON.stringify(users));
    renderUsersTable();
}

// === Админ: отобразить таблицу пользователей ===
function renderUsersTable() {
    let table = document.getElementById("usersTable");
    if (!table) return;

    let users = JSON.parse(localStorage.getItem("users") || "[]");
    table.innerHTML = "";

    users.forEach(u => {
        if (u.login === "admin") return; // не показываем супер-админа

        let tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${u.login}</td>
            <td>
                <select onchange="changeRole('${u.login}', this.value)" class="form-select form-select-sm">
                    <option value="worker" ${u.role==='worker'?'selected':''}>Worker</option>
                    <option value="manager" ${u.role==='manager'?'selected':''}>Manager</option>
                </select>
            </td>
            <td><button class="btn btn-danger btn-sm" onclick="deleteUser('${u.login}')">Удалить</button></td>
        `;
        table.appendChild(tr);
    });
}
