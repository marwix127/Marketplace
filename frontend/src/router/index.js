import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import ProductDetail from "../views/ProductDetail.vue";
import ProductEdit from "../views/ProductEdit.vue";
import AddProduct from "../views/AddProducts.vue";
import Cart from "../views/Cart.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  {
  path: "/product/:id",
  name: "ProductDetail",
  component: ProductDetail,
},
{
  path: "/products/:id/edit",
  name: "ProductEdit",
  component: ProductEdit,
},
{
  path: "/products/add",
  name: "AddProduct",
  component: AddProduct,
},
{
  path: "/cart",
  name: "Cart",
  component: Cart,
},


];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
