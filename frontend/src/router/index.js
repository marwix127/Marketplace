import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import ProductDetail from "../views/ProductDetail.vue";
import ProductEdit from "../views/ProductEdit.vue";
import AddProduct from "../views/AddProducts.vue";
import Cart from "../views/Cart.vue";
import Orders from "../views/Orders.vue";

// meta.requiresAuth: only for logged-in users. meta.guestOnly: only for anonymous users
const routes = [
  { path: "/", component: Home },
  { path: "/login", component: Login, meta: { guestOnly: true } },
  { path: "/register", component: Register, meta: { guestOnly: true } },
  {
    path: "/product/:id",
    name: "ProductDetail",
    component: ProductDetail,
  },
  {
    path: "/products/:id/edit",
    name: "ProductEdit",
    component: ProductEdit,
    meta: { requiresAuth: true },
  },
  {
    path: "/products/add",
    name: "AddProduct",
    component: AddProduct,
    meta: { requiresAuth: true },
  },
  {
    path: "/cart",
    name: "Cart",
    component: Cart,
    meta: { requiresAuth: true },
  },
  {
    path: "/orders",
    name: "Orders",
    component: Orders,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const isAuthenticated = !!localStorage.getItem("access");

  if (to.meta.requiresAuth && !isAuthenticated) {
    // Come back to the requested page after logging in
    return { path: "/login", query: { redirect: to.fullPath } };
  }
  if (to.meta.guestOnly && isAuthenticated) {
    return "/";
  }
});

export default router;
