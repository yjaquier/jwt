<script setup lang="ts">
import { ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome' // Import font awesome icon component

const registrationForm = ref({
  firstname: 'Yannick',
  lastname: 'Jaquier',
  username: 'yjaquier',
  password: 'secure_password',
})

const showPassword = ref(true)

function toggleShow() {
  showPassword.value = !showPassword.value;
}

async function register(): Promise<object[] | object> {
  // const data=new FormData()
  // data.append('firstname', registrationForm.value.firstname)
  // data.append('lastname', registrationForm.value.lastname)
  // data.append('username', registrationForm.value.username)
  // data.append('password', registrationForm.value.password)
  return await fetch('http://localhost:8181/register', {
    method: 'POST',
    headers: { 'content-type': 'application/json'},
    body: JSON.stringify({ 'firstname': registrationForm.value.firstname, 'lastname': registrationForm.value.lastname, 'username': registrationForm.value.username, 'password': registrationForm.value.password })
  }).then(async response => {
    // console.log(response)
    if (!response.ok) {
      const msg = await response.json()
      // console.log(msg)
      window.alert("Registration failed !\n" + msg.detail.Error)
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
    console.log(data)
    return data
  }).catch(error => {
    console.log('Problem while running /register fastAPI endpoint:\n', error);
    // window.alert("Registration failed !")
    return []
  })
}

</script>

<template>
  <main>
    <section>
      <h1>Register a new account</h1>
    </section>

      <fieldset class="flex-container">
        <legend>User registration</legend>

        <label>
          <span>Firstname: </span>
          <input
            v-model="registrationForm.firstname"
            autocomplete="given-name"
            name="firstname"
            placeholder="John"
            required
            type="text"
          />
        </label>

        <label>
          <span>Lastname: </span>
          <input
            v-model="registrationForm.lastname"
            autocomplete="family-name"
            name="lastname"
            placeholder="Doe"
            required
            type="text"
          />
        </label>

        <label>
          <span>Username: </span>
          <input
            v-model="registrationForm.username"
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
              v-model="registrationForm.password"
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
              v-model="registrationForm.password"
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
          <button @click="register">Register</button>
          <button @click="$router.push('/login')">Login</button>
          <button @click="$router.push('/')">Home</button>
        </div>
      </fieldset>
 

  </main>
</template>