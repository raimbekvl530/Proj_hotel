// === Проверка текущего пользователя ===
function getCurrentUser() {
    return JSON.parse(localStorage.getItem("currentUser") || "null");
}

// === Logout ===
function logout() {
    localStorage.removeItem("currentUser");
    location.href = "login.html";
}

// === Users ===
function getUsers() {
    return JSON.parse(localStorage.getItem("users") || "[]");
}
function saveUsers(users) {
    localStorage.setItem("users", JSON.stringify(users));
}

// === Админ: создаём супер-админа, если нет ===
let users = getUsers();
if (!users.some(u => u.login === "admin")) {
    users.push({login:"admin", pass:"admin", role:"admin"});
    saveUsers(users);
}

// === Рендер таблицы пользователей для админа ===
function renderUsersTable() {
    let tbody = document.querySelector("#usersTable tbody");
    tbody.innerHTML = "";
    getUsers().forEach((u,i)=>{
        let tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${u.login}</td>
            <td>${u.role}</td>
            <td>
                <button class="btn btn-sm btn-danger" onclick="deleteUser(${i})">Удалить</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function deleteUser(index) {
    if (!confirm("Удалить пользователя?")) return;
    let users = getUsers();
    users.splice(index,1);
    saveUsers(users);
    renderUsersTable();
}

// === Товары ===
function getProducts() { return JSON.parse(localStorage.getItem("products")||"[]"); }
function saveProducts(products) { localStorage.setItem("products", JSON.stringify(products)); }

function renderProductsTable() {
    let tbody = document.querySelector("#productsTable tbody");
    tbody.innerHTML = "";
    getProducts().forEach((p,i)=>{
        let tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${p.name}</td>
            <td>${p.qty}</td>
            <td>
                <button class="btn btn-sm btn-warning" onclick="editProduct(${i})">Редактировать</button>
                <button class="btn btn-sm btn-danger" onclick="deleteProduct(${i})">Удалить</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

document.getElementById("productForm").addEventListener("submit", function(e){
    e.preventDefault();
    let products = getProducts();
    let name = document.getElementById("productName").value;
    let qty = parseInt(document.getElementById("productQty").value);
    let editIndex = document.getElementById("editIndex").value;

    if(editIndex==="") products.push({name,qty});
    else products[editIndex] = {name, qty};

    saveProducts(products);
    renderProductsTable(); // <-- таблица обновляется сразу
    this.reset();
    document.getElementById("editIndex").value="";
    bootstrap.Modal.getInstance(document.getElementById('addProductModal')).hide();
});

function editProduct(i){
    let p = getProducts()[i];
    document.getElementById("productName").value = p.name;
    document.getElementById("productQty").value = p.qty;
    document.getElementById("editIndex").value = i;
}

function deleteProduct(i){
    if(!confirm("Удалить этот товар?")) return;
    let products = getProducts();
    products.splice(i,1);
    saveProducts(products);
    renderProductsTable();
}

// === Поставщики ===
function getSuppliers() { return JSON.parse(localStorage.getItem("suppliers")||"[]"); }
function saveSuppliers(suppliers) { localStorage.setItem("suppliers", JSON.stringify(suppliers)); }

function renderSuppliersTable() {
    let tbody = document.querySelector("#suppliersTable tbody");
    tbody.innerHTML = "";
    getSuppliers().forEach((s,i)=>{
        let tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${s.name}</td>
            <td>
                <button class="btn btn-sm btn-warning" onclick="editSupplier(${i})">Редактировать</button>
                <button class="btn btn-sm btn-danger" onclick="deleteSupplier(${i})">Удалить</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

document.getElementById("supplierForm").addEventListener("submit", function(e){
    e.preventDefault();
    let suppliers = getSuppliers();
    let name = document.getElementById("supplierName").value;
    let editIndex = document.getElementById("editSupplierIndex").value;

    if(editIndex==="") suppliers.push({name});
    else suppliers[editIndex] = {name};

    saveSuppliers(suppliers);
    renderSuppliersTable(); // <-- таблица обновляется
    this.reset();
    document.getElementById("editSupplierIndex").value="";
    bootstrap.Modal.getInstance(document.getElementById('addSupplierModal')).hide();
});

function editSupplier(i){
    let s = getSuppliers()[i];
    document.getElementById("supplierName").value = s.name;
    document.getElementById("editSupplierIndex").value = i;
}

function deleteSupplier(i){
    if(!confirm("Удалить этого поставщика?")) return;
    let suppliers = getSuppliers();
    suppliers.splice(i,1);
    saveSuppliers(suppliers);
    renderSuppliersTable();
}

// === Поставки ===
function getSupplies() { return JSON.parse(localStorage.getItem("supplies")||"[]"); }
function saveSupplies(supplies) { localStorage.setItem("supplies", JSON.stringify(supplies)); }

function renderSuppliesTable(){
    let tbody = document.querySelector("#supplyTable tbody");
    tbody.innerHTML = "";
    getSupplies().forEach((s,i)=>{
        let tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${s.product}</td>
            <td>${s.supplier}</td>
            <td>${s.qty}</td>
            <td>${s.date}</td>
            <td>
                <button class="btn btn-sm btn-danger" onclick="deleteSupply(${i})">Удалить</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

document.getElementById("supplyForm").addEventListener("submit", function(e){
    e.preventDefault();
    let supplies = getSupplies(); // <-- берём текущие, а не создаём новый массив
    let product = document.getElementById("supplyProduct").value;
    let supplier = document.getElementById("supplySupplier").value;
    let qty = parseInt(document.getElementById("supplyQty").value);
    let date = document.getElementById("supplyDate").value;

    supplies.push({product, supplier, qty, date});
    saveSupplies(supplies);
    renderSuppliesTable(); // <-- таблица обновляется сразу

    this.reset();
    bootstrap.Modal.getInstance(document.getElementById('addSupplyModal')).hide();
});

function deleteSupply(i){
    if(!confirm("Удалить эту поставку?")) return;
    let supplies = getSupplies();
    supplies.splice(i,1);
    saveSupplies(supplies);
    renderSuppliesTable();
}

// === Заполнение селектов при открытии модального окна поставки ===
document.getElementById("addSupplyModal").addEventListener("show.bs.modal", function(){
    let productSelect = document.getElementById("supplyProduct");
    productSelect.innerHTML="";
    getProducts().forEach(p=>{
        let option = document.createElement("option");
        option.value = p.name;
        option.text = p.name;
        productSelect.add(option);
    });

    let supplierSelect = document.getElementById("supplySupplier");
    supplierSelect.innerHTML="";
    getSuppliers().forEach(s=>{
        let option = document.createElement("option");
        option.value = s.name;
        option.text = s.name;
        supplierSelect.add(option);
    });
});

// === Инициализация страницы ===
document.addEventListener("DOMContentLoaded", function(){
    let user = getCurrentUser();
    if(!user){
        alert("Сначала войдите в систему!");
        location.href = "login.html";
        return;
    }

    document.getElementById("welcome").innerHTML =
        `Вы вошли как <b>${user.login}</b> (роль: ${user.role})`;

    if(user.role==="admin") {
        document.getElementById("adminBlock").style.display="block";
        renderUsersTable();
    }

    renderProductsTable();
    renderSuppliersTable();
    renderSuppliesTable();
});
