<script setup lang="ts">
import { ref } from 'vue'
import { onMounted } from 'vue'
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome' // Import font awesome icon component

// const loginForm = ref({
//   username: 'yjaquier',
//   password: 'secure_password',
// })

// function loginUser() {
//   // registeredFullName.value = `${loginForm.username.trim()}`
//   loginForm.password = ''
// }

const isAuthenticated = ref(false)
const fullname = ref(null)

async function getUserInformation(): Promise<object[] | object> {
  return await fetch('http://localhost:8181/', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
  }).then(response => {
    // console.log(response)
    if (!response.ok) {
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
    isAuthenticated.value = true
    fullname.value = data.fullname
    return data
  }).catch(error => {
    console.log('Problem requesting fastAPI home page:\n', error);
    return []
  })
}

onMounted(() => {
  getUserInformation()
})

function logout() {
  localStorage.removeItem('token')
  isAuthenticated.value = false
  fullname.value = null
}
</script>

<template>
  <main>
    <section>
      <h1>Home Page</h1>
    </section>

    <fieldset class="flex-container">
      <legend>User Information</legend>
      <div>
        <span>Authenticated ?: {{ isAuthenticated }}</span>
      </div>
      <div v-if="fullname !== null">
        <span>How are you {{ fullname }} today ?</span>
      </div>
      <div v-if="!isAuthenticated">
        <button @click="$router.push('/register')">Register</button>
        <button @click="$router.push('/login')">Login</button>
      </div>
      <div v-else>
        <button @click="$router.push('/todos')">Todos</button>
        <button @click="logout">Logout</button>
      </div>
    </fieldset>
  </main>
</template>

<style scoped lang="scss">

</style>