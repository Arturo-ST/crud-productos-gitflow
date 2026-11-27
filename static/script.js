const form=document.getElementById('productForm');
const rows=document.getElementById('productRows');
const message=document.getElementById('message');
let products=[];
function notice(text, error=false){message.textContent=text;message.className=error?'error':'ok';}
async function request(url,options={}){
  const response=await fetch(url,{...options,headers:{'Content-Type':'application/json'}});
  const body=await response.json();
  if(!response.ok)throw new Error(body.error||'Error de solicitud');
  return body;
}
const money=value=>new Intl.NumberFormat('es-DO',{style:'currency',currency:'DOP'}).format(value);
function resetForm(){form.reset();document.getElementById('productId').value='';document.getElementById('formTitle').textContent='Nuevo producto';document.getElementById('saveBtn').textContent='Guardar producto';document.getElementById('cancelBtn').hidden=true;}
function showProducts(){
  rows.replaceChildren();
  if(!products.length){const row=rows.insertRow();const td=row.insertCell();td.colSpan=6;td.className='empty';td.textContent='No hay productos registrados';return;}
  for(const p of products){
    const row=rows.insertRow();
    for(const value of [p.id,p.nombre,p.descripcion,money(p.precio),p.cantidad])row.insertCell().textContent=value;
    const actions=row.insertCell();
    const edit=document.createElement('button');edit.type='button';edit.textContent='Editar';edit.className='secondary';edit.onclick=()=>editProduct(p.id);
    const remove=document.createElement('button');remove.type='button';remove.textContent='Eliminar';remove.className='danger';remove.onclick=()=>deleteProduct(p.id);
    actions.append(edit,remove);
  }
}
async function loadProducts(){try{products=(await request('/api/productos')).productos;showProducts();}catch(err){notice(err.message,true);}}
function editProduct(id){
  const p=products.find(x=>x.id===id);if(!p)return;
  for(const key of ['nombre','descripcion','precio','cantidad'])document.getElementById(key).value=p[key];
  document.getElementById('productId').value=id;document.getElementById('formTitle').textContent='Editar producto';document.getElementById('saveBtn').textContent='Guardar cambios';document.getElementById('cancelBtn').hidden=false;window.scrollTo({top:0,behavior:'smooth'});
}
async function deleteProduct(id){
  if(!confirm('¿Eliminar este producto?'))return;
  try{await request('/api/productos/'+id,{method:'DELETE'});notice('Producto eliminado');await loadProducts();}catch(err){notice(err.message,true);}
}
form.addEventListener('submit',async event=>{
  event.preventDefault();
  const id=document.getElementById('productId').value;
  const payload={nombre:document.getElementById('nombre').value,descripcion:document.getElementById('descripcion').value,precio:Number(document.getElementById('precio').value),cantidad:Number(document.getElementById('cantidad').value)};
  try{await request(id?'/api/productos/'+id:'/api/productos',{method:id?'PUT':'POST',body:JSON.stringify(payload)});notice(id?'Producto actualizado':'Producto registrado');resetForm();await loadProducts();}catch(err){notice(err.message,true);}
});
document.getElementById('cancelBtn').onclick=resetForm;
document.getElementById('refreshBtn').onclick=loadProducts;
loadProducts();
