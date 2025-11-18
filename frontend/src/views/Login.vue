<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>Inicia Sesión</h1>
        <p class="text-subtitle">Accede a tu cuenta de MarketPlace</p>
      </div>

      <form @submit.prevent="login" class="auth-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="tu@email.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Contraseña</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="••••••••"
            required
          />
        </div>

        <button type="submit" class="btn-primary">Entrar</button>
      </form>

      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <p class="auth-footer">
        ¿No tienes cuenta?
        <router-link to="/register" class="link-primary">Regístrate aquí</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../api/axios";
import { useToast } from "../composables/useToast";

const router = useRouter();
const { error: showError, success: showSuccess } = useToast();

const email = ref("");
const password = ref("");

const login = async () => {
  try {
    const response = await api.post("/users/login/", {
      email: email.value,
      password: password.value,
    });

    const access = response.data.access;
    const refresh = response.data.refresh;

    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);

    const userResponse = await api.get("/users/me/", {
      headers: { Authorization: `Bearer ${access}` },
    });

    localStorage.setItem("username", userResponse.data.username);
    localStorage.setItem("email", userResponse.data.email);

    window.dispatchEvent(new Event("auth-changed"));

    showSuccess("¡Sesión iniciada correctamente!");
    setTimeout(() => router.push("/"), 500);
  } catch (err) {
    console.error("Error logging in:", err);
    showError(err.response?.data?.detail || "Error al iniciar sesión");
  }
};
</script>

<style>
:root {
  --primary-color: #2563eb;
  --error-color: #dc2626;
  --text-dark: #1f2937;
  --text-light: #6b7280;
  --bg-light: #f9fafb;
  --border-color: #e5e7eb;
  --shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 2rem 1rem;
}

.auth-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: var(--shadow);
  padding: 3rem;
  width: 100%;
  max-width: 420px;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-header h1 {
  font-size: 1.875rem;
  color: var(--text-dark);
  margin: 0 0 0.5rem 0;
}

.text-subtitle {
  color: var(--text-light);
  margin: 0;
  font-size: 0.95rem;
}

.auth-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-dark);
  font-size: 0.95rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, var(--primary-color) 0%, #1e40af 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px rgba(37, 99, 235, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
}

.alert {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.alert-error {
  background-color: #fee2e2;
  color: var(--error-color);
  border: 1px solid #fecaca;
}

.auth-footer {
  text-align: center;
  color: var(--text-light);
  font-size: 0.95rem;
  margin: 0;
}

.link-primary {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  transition: opacity 0.3s ease;
}

.link-primary:hover {
  opacity: 0.8;
  text-decoration: underline;
}
</style>
