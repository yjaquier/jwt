<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome' // Import font awesome icon component

const router = useRouter()

const loginForm = ref({
  username: 'yjaquier',
  password: 'secure_password',
})

const showPassword = ref(true)

function toggleShow() {
  showPassword.value = !showPassword.value;
}

async function login(): Promise<object[] | object> {
  return await fetch('http://localhost:8181/login', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ 'username': loginForm.value.username, 'password': loginForm.value.password })
  }).then(async response => {
    // console.log(response)
    if (!response.ok) {
      const msg = await response.json()
      // console.log(msg)
      window.alert("Login failed !\n" + msg.detail.Error)
      throw new Error(response.statusText);
    }
    else {
      // Handling empty response .json() function on an empty response generate below error
      // Uncaught SyntaxError: Unexpected end of JSON input
      return response.json().catch((error) => {
        console.log('Empty response from API call: ' + error)
        return null
      })
    }
  }).then(data => {
    // console.log(data)
    if (data && data.access_token) {
      localStorage.setItem('token', data.access_token)
      router.push('/')
      }
    // else
    //   window.alert("Login failed !")
    return data
    }).catch(error => {
    console.log("Problem while running /login fastAPI endpoint:\n", error)
    return []
  })
}
</script>

<template>
  <main>
    <section>
      <h1>Login User</h1>
    </section>

    <fieldset class="flex-container">
      <legend>User login</legend>

      <label>
        <span>Username: </span>
        <input
          v-model="loginForm.username"
          autocomplete="username"
          name="username"
          placeholder="JohnDoe"
          required
          type="text"
        />
      </label>

      <label>
        <div v-if="showPassword">
          <span>Password: </span>
          <input 
            v-model="loginForm.password"
            autocomplete="current-password"
            name="password"
            placeholder="Enter a password"
            required
            type="password"
          />
          <font-awesome-icon icon="fa-regular fa-eye" @click="toggleShow" />
        </div>
        <div v-else>
          <span>Password: </span>
          <input
            v-model="loginForm.password"
            autocomplete="current-password"
            name="password"
            placeholder="Enter a password"
            required
            type="text"
          />
          <font-awesome-icon icon="fa-regular fa-eye-slash" @click="toggleShow" />
        </div> 
      </label>

      <div>
        <button @click="login">Login</button>
        <button @click="router.push('/register')">Register</button>
        <button @click="router.push('/')">Home</button>
      </div>
    </fieldset>
  </main>
</template>

<style scoped lang="scss">

</style>