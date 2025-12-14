<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>Crea tu Cuenta</h1>
        <p class="text-subtitle">Únete a MarketPlace hoy</p>
      </div>

      <form @submit.prevent="register" class="auth-form">
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
          <label for="username">Nombre de usuario</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="tu_usuario"
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

        <button type="submit" class="btn-primary">Registrarse</button>
      </form>

      <div v-if="errorMsg" class="alert alert-error">
        {{ errorMsg }}
      </div>

      <p class="auth-footer">
        ¿Ya tienes cuenta?
        <router-link to="/login" class="link-primary">Inicia sesión aquí</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../api/axios";
import { useToast } from "../composables/useToast";

const { error: showError, success: showSuccess } = useToast();

const email = ref("");
const username = ref("");
const password = ref("");
const errorMsg = ref("");

const register = async () => {
  errorMsg.value = "";
  try {
    const response = await api.post("/users/register/", {
      email: email.value,
      username: username.value,
      password: password.value,
    });

    showSuccess("¡Cuenta creada correctamente! Ya puedes iniciar sesión.");
    email.value = "";
    username.value = "";
    password.value = "";
    // Opcional: Redirigir al login tras unos segundos
    // setTimeout(() => router.push('/login'), 2000);
  } catch (err) {
    console.error("Error registering:", err);
    let msg = "Error al registrar usuario.";
    
    if (err.response && err.response.data) {
        const data = err.response.data;
        // Si es un error de detalle simple
        if (data.detail) {
            msg = data.detail;
        } 
        // Si es un error de validación de campos (password, username, email...)
        else {
            // Unimos los mensajes de error de los campos
            const fieldErrors = Object.values(data).flat();
            if (fieldErrors.length > 0) {
                msg = fieldErrors.join(" ");
            }
        }
    }
    
    errorMsg.value = msg;
    showError(msg);
  }
};
</script>

<style>
:root {
  --primary-color: #2563eb;
  --error-color: #dc2626;
  --success-color: #16a34a;
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

.alert-success {
  background-color: #dcfce7;
  color: var(--success-color);
  border: 1px solid #bbf7d0;
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
